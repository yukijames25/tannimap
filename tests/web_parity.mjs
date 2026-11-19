// Runs the browser version's core (the <script id="core"> in web/index.html) on cases read from stdin
// and prints its canonical results, so tests/test_web.py can compare them with the Python version.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));
const html = readFileSync(join(here, "..", "web", "index.html"), "utf8");
const m = html.match(/<script id="core">([\s\S]*?)<\/script>/);
if (!m) throw new Error("core script not found");
const TANNIMAP = new Function(m[1] + "\nreturn TANNIMAP;")();

const cases = JSON.parse(readFileSync(0, "utf8"));
const out = cases.map(c => {
  try {
    const r = TANNIMAP.loadRules(c.rules);
    let courses = TANNIMAP.parseTranscript(c.grades, r);
    if (c.plan) courses = courses.concat(TANNIMAP.parseTranscript(c.plan, r, TANNIMAP.PLANNED));
    const res = TANNIMAP.check(r, courses, c.years || null, c.entry_year || null);
    return { ok: TANNIMAP.canonical(r, res), text: TANNIMAP.textReport(r, res, courses) };
  } catch (e) {
    return { error: e.constructor.name + ": " + e.message };
  }
});
process.stdout.write(JSON.stringify(out));
