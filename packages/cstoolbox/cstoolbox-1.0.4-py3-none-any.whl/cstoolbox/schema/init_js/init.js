const originalQuery = window.navigator.permissions.query;
window.navigator.permissions.query = (parameters) =>
  parameters.name === "notifications"
    ? Promise.resolve({ state: Notification.permission })
    : originalQuery(parameters);
Object.defineProperty(navigator, "webdriver", {
  get: () => false,
});