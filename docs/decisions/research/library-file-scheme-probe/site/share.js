// a/index.html は findsummits:probe-a に時刻を書き、b/index.html はそれを読む（P10）。普通の script（DEC130）。
"use strict";

(function () {
  var KEY = "findsummits:probe-a";
  var role = document.body.getAttribute("data-role");
  var answer = document.getElementById("answer");
  var out = { userAgent: navigator.userAgent, protocol: location.protocol, page: role, time: new Date().toString() };
  try {
    var ls = window.localStorage;
    if (role === "a") {
      var v = "a が書いた時刻 " + new Date().toString();
      ls.setItem(KEY, v);
      out.wrote = v;
      answer.textContent = "書いた";
    } else {
      var got = ls.getItem(KEY);
      out.read = got;
      answer.textContent = got ? "見えた" : "見えない";
    }
  } catch (e) {
    out.error = String(e);
    answer.textContent = "localStorage を使えない";
  }
  document.getElementById("json").value = JSON.stringify(out, null, 1);
})();
