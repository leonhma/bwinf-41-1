const { writeFileSync, readFileSync } = require("fs");
const { join } = require("path");

const file = readFileSync(
  join(__dirname, "../node_modules/@smui/snackbar/package.json")
);
const json = JSON.parse(file);
json["exports"]["./bare.css"] = "./bare.css";
writeFileSync(
  join(__dirname, "../node_modules/@smui/snackbar/package.json"),
  JSON.stringify(json, null, 2)
);
