import { gzipSync } from 'node:zlib'
import { readdirSync, readFileSync, statSync } from 'node:fs'
import { join } from 'node:path'

const distAssetsDir = join(process.cwd(), 'dist', 'assets')

const maxMainJsBytes = Number(process.env.BUNDLE_MAX_MAIN_JS_BYTES || 130 * 1024)
const maxMainJsGzipBytes = Number(process.env.BUNDLE_MAX_MAIN_JS_GZIP_BYTES || 50 * 1024)
const maxMainCssBytes = Number(process.env.BUNDLE_MAX_MAIN_CSS_BYTES || 30 * 1024)
const maxMainCssGzipBytes = Number(process.env.BUNDLE_MAX_MAIN_CSS_GZIP_BYTES || 8 * 1024)

const files = readdirSync(distAssetsDir)

const findMainAsset = (ext) =>
  files
    .filter((file) => file.startsWith('index-') && file.endsWith(ext))
    .sort((a, b) => statSync(join(distAssetsDir, b)).mtimeMs - statSync(join(distAssetsDir, a)).mtimeMs)[0]

const formatKb = (value) => `${(value / 1024).toFixed(2)} KiB`

const checkAsset = ({ fileName, maxBytes, maxGzipBytes, label }) => {
  if (!fileName) {
    throw new Error(`Missing ${label} bundle in dist/assets`) 
  }

  const filePath = join(distAssetsDir, fileName)
  const buffer = readFileSync(filePath)
  const gzipSize = gzipSync(buffer).length

  console.log(`${label}: ${fileName}`)
  console.log(`  raw:  ${formatKb(buffer.length)} (budget ${formatKb(maxBytes)})`)
  console.log(`  gzip: ${formatKb(gzipSize)} (budget ${formatKb(maxGzipBytes)})`)

  const errors = []
  if (buffer.length > maxBytes) {
    errors.push(`raw size exceeds budget by ${formatKb(buffer.length - maxBytes)}`)
  }
  if (gzipSize > maxGzipBytes) {
    errors.push(`gzip size exceeds budget by ${formatKb(gzipSize - maxGzipBytes)}`)
  }

  return errors
}

const mainJs = findMainAsset('.js')
const mainCss = findMainAsset('.css')

const failures = [
  ...checkAsset({
    fileName: mainJs,
    maxBytes: maxMainJsBytes,
    maxGzipBytes: maxMainJsGzipBytes,
    label: 'Main JS',
  }),
  ...checkAsset({
    fileName: mainCss,
    maxBytes: maxMainCssBytes,
    maxGzipBytes: maxMainCssGzipBytes,
    label: 'Main CSS',
  }),
]

if (failures.length) {
  console.error('\nBundle budget check failed:')
  for (const failure of failures) {
    console.error(`- ${failure}`)
  }
  process.exit(1)
}

console.log('\nBundle budget check passed.')
