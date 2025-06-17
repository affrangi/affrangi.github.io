function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}

function exportBib2Txt() {
  const bibItems = document.querySelectorAll(".bibliography > li");
  let bibText = "";
  for (const item of bibItems) {
    if (!item.classList.contains("unloaded")) {
      bibText += '\n\n' + item.querySelector('.bib-citation-txt').innerText;
    }
  }

  download("exportBib.txt", bibText.trim());
}

window.exportBib2Txt = exportBib2Txt;

function exportBib() {
  const bibItems = document.querySelectorAll(".bibliography > li");
  let bibTexCode = "";
  let bibTexCodeContainer = null;
  for (const item of bibItems) {
    if (!item.classList.contains("unloaded")) {
      bibTexCodeContainer = item.querySelector('.bibtex-code');
      if (bibTexCodeContainer) {
        bibTexCode += '\n\n' + item.querySelector('.bibtex-code').innerText;
      }
    }
  }

  download("exportBib.bib", bibTexCode.trim());
}

window.exportBib = exportBib;