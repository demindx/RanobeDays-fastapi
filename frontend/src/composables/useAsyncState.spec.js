import { describe, expect, it } from 'vitest'
import { useAsyncState } from './useAsyncState'

const deferred = () => {
  let resolve
  const promise = new Promise((done) => {
    resolve = done
  })
  return { promise, resolve }
}

describe('useAsyncState', () => {
  it('ignores an obsolete result and keeps loading until the latest run settles', async () => {
    const first = deferred()
    const second = deferred()
    const { loading, run } = useAsyncState()

    const firstRun = run(() => first.promise)
    const secondRun = run(() => second.promise)

    first.resolve('obsolete')
    await expect(firstRun).resolves.toBeNull()
    expect(loading.value).toBe(true)

    second.resolve('current')
    await expect(secondRun).resolves.toBe('current')
    expect(loading.value).toBe(false)
  })
})
