const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function(app) {
  app.use(
    "/api",
    createProxyMiddleware({
      target: "http://localhost:8090",
      changeOrigin: true,
    }),
  );

  app.use(
    "/backend",
    createProxyMiddleware({
      target: "http://localhost:5000",
      changeOrigin: true,
    }),
  );
};
