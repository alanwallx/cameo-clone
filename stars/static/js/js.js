function copyText() {
  var copyText = document.getElementById("videoURL");
  copyText.select();
  copyText.setSelectionRange(0, 99999);
  document.execCommand("copy");

  var tooltip = document.getElementById("isvTooltip");
  tooltip.innerHTML = "Copied to clipboard";
}

function outFunc() {
  var tooltip = document.getElementById("isvTooltip");
  tooltip.innerHTML = "Copy to clipboard";
}


// If hide button is clicked, hide the post
document.addEventListener('click', event => {
    const element = event.target;
    if (element.className === 'hide') {
        element.parentElement.remove();

    }
});
