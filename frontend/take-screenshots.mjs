
import { chromium } from "playwright";
import fs from "node:fs";

const BASE_URL = "http://localhost:5173";
const OUT = "../screenshots";

fs.mkdirSync(OUT, { recursive: true });

const pages = [
  { name: "02_login.png", path: "/login" },
  { name: "10_patient_dashboard.png", path: "/patient/dashboard" },
  { name: "16b_smart_upload_extracted_json_review.png", path: "/documents/upload" },
  { name: "15b_ai_assistant_report_explanation.png", path: "/ai-assistant" },
  { name: "14b_patient_medications_after_save.png", path: "/medications" },
];

const browser = await chromium.launch({ headless: false });
const page = await browser.newPage({
  viewport: { width: 1440, height: 1000 },
  deviceScaleFactor: 1,
});

for (const item of pages) {
  try {
    await page.goto(BASE_URL + item.path, {
      waitUntil: "domcontentloaded",
      timeout: 20000,
    });

    await page.waitForTimeout(2000);

    await page.screenshot({
      path: `${OUT}/${item.name}`,
      fullPage: true,
    });

    console.log(`Saved: ${item.name}`);
  } catch (error) {
    console.error(`Failed: ${item.path}`, error.message);
  }
}

await browser.close();
