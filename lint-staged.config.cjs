const quote = (value) => `'${value.replace(/'/g, `'\\''`)}'`

const toFrontendRelative = (files) =>
  files
    .filter((file) => file.startsWith('frontend/'))
    .map((file) => file.replace(/^frontend\//, ''))

module.exports = {
  'frontend/**/*.{js,vue}': (files) => {
    const rel = toFrontendRelative(files)
    if (!rel.length) return []
    return [`cd frontend && bunx eslint --fix --max-warnings=0 ${rel.map(quote).join(' ')}`]
  },
  'frontend/**/*.{css,md,json}': (files) => {
    const rel = toFrontendRelative(files)
    if (!rel.length) return []
    return [`cd frontend && bunx prettier --write ${rel.map(quote).join(' ')}`]
  },
}
