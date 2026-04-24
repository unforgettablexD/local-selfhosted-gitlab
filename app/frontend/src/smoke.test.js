import test from "node:test";
import assert from "node:assert/strict";
import { appBanner } from "./index.js";

test("frontend smoke test", () => {
  assert.equal(
    appBanner(),
    "Self-hosted GitLab DevSecOps platform frontend placeholder"
  );
});
