import http from "node:http";
import { readFile } from "node:fs/promises";
import { appBanner } from "./index.js";

const PORT = Number(process.env.PORT || 4173);

const services = [
  { id: "backendHealth", label: "Backend Health", url: "http://localhost:8000/health", expected: 200 },
  { id: "backendDocs", label: "Backend Docs", url: "http://localhost:8000/docs", expected: 200 },
  { id: "prometheus", label: "Prometheus", url: "http://localhost:9090/-/healthy", expected: 200 },
  { id: "grafana", label: "Grafana", url: "http://localhost:3000/api/health", expected: 200 },
  { id: "gitlab", label: "GitLab", url: "http://localhost:8080/users/sign_in", expected: 200 }
];

async function checkService(service) {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 4000);
    const response = await fetch(service.url, { signal: controller.signal });
    clearTimeout(timeout);
    return {
      ...service,
      ok: response.status === service.expected,
      status: response.status
    };
  } catch (_error) {
    return {
      ...service,
      ok: false,
      status: "offline"
    };
  }
}

const server = http.createServer(async (req, res) => {
  if (!req.url) {
    res.writeHead(400);
    res.end("Bad request");
    return;
  }

  if (req.url === "/api/checks") {
    const checks = await Promise.all(services.map((service) => checkService(service)));
    const body = JSON.stringify({
      banner: appBanner(),
      checks
    });
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(body);
    return;
  }

  if (req.url === "/" || req.url === "/index.html") {
    const html = await readFile(new URL("./dashboard.html", import.meta.url), "utf8");
    res.writeHead(200, { "Content-Type": "text/html; charset=utf-8" });
    res.end(html);
    return;
  }

  res.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
  res.end("Not Found");
});

server.listen(PORT, () => {
  console.log(`${appBanner()} dashboard running on http://localhost:${PORT}`);
});
