export const trackUiEvent = (eventName, payload = {}) => {
  if (import.meta.env.DEV) {
    console.info(`[analytics] ${eventName}`, payload)
  }
}
