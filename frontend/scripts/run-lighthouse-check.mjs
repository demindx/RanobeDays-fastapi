import { spawn } from 'node:child_process'
import { once } from 'node:events'
import { setTimeout as wait } from 'node:timers/promises'
import { access, readFile } from 'node:fs/promises'

const host = process.env.LH_HOST || '127.0.0.1'
const port = process.env.LH_PORT || '4274'
const url = `http://${host}:${port}`
const reportPath = './dist/lighthouse-mobile.json'
const performanceThreshold = Number(process.env.LH_PERF_THRESHOLD || 85)
const accessibilityThreshold = Number(process.env.LH_A11Y_THRESHOLD || 90)

const run = (cmd, args, opts = {}) =>
  new Promise((resolve, reject) => {
    const child = spawn(cmd, args, {
      stdio: 'inherit',
      shell: false,
      ...opts,
    })

    child.on('error', reject)
    child.on('exit', (code) => {
      if (code === 0) resolve()
      else reject(new Error(`${cmd} ${args.join(' ')} failed with code ${code}`))
    })
  })

const isReady = async () => {
  try {
    const response = await fetch(url)
    return response.ok
  } catch {
    return false
  }
}

const waitForServer = async (timeoutMs = 30_000) => {
  const started = Date.now()
  while (Date.now() - started < timeoutMs) {
    if (await isReady()) {
      return
    }
    await wait(500)
  }
  throw new Error(`Preview server did not start within ${timeoutMs}ms`)
}

const preview = spawn('bun', ['run', 'preview', '--host', host, '--port', String(port)], {
  stdio: 'inherit',
  shell: false,
})

preview.on('error', (error) => {
  console.error(error)
  process.exit(1)
})

try {
  await waitForServer()

  const chromePath = process.env.LIGHTHOUSE_CHROME_PATH
  const chromePathArgs = chromePath ? ['--chrome-path', chromePath] : []

  await run('bunx', [
    'lighthouse',
    url,
    '--quiet',
    '--chrome-flags=--headless --no-sandbox',
    '--only-categories=performance,accessibility',
    '--output=json',
    '--output-path',
    reportPath,
    ...chromePathArgs,
  ])

  await access(reportPath)
  const reportRaw = await readFile(reportPath, 'utf-8')
  const report = JSON.parse(reportRaw)

  const performance = Math.round((report.categories.performance?.score ?? 0) * 100)
  const accessibility = Math.round((report.categories.accessibility?.score ?? 0) * 100)

  console.log(`Lighthouse (mobile): performance=${performance}, accessibility=${accessibility}`)

  const failures = []
  if (performance < performanceThreshold) {
    failures.push(`Performance ${performance} < ${performanceThreshold}`)
  }
  if (accessibility < accessibilityThreshold) {
    failures.push(`Accessibility ${accessibility} < ${accessibilityThreshold}`)
  }

  if (failures.length) {
    console.error('Lighthouse thresholds failed:')
    for (const failure of failures) {
      console.error(`- ${failure}`)
    }
    process.exitCode = 1
  }
} finally {
  preview.kill('SIGTERM')
  await once(preview, 'exit').catch(() => {})
}
