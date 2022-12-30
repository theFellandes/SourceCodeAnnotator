let chooseFileButton = document.querySelector("#fileUpload");
let sourceOutput = document.querySelector("#sourceOutput");
let sourceText = document.querySelector("#sourceText");
let lazyDocButton = document.querySelector("#lazyDocButton");
let inputForm = document.querySelector("#inputForm");

lazyDocButton.addEventListener("click", function () {
    inputForm.submit();
});

chooseFileButton.addEventListener("change", function () {
    let fr = new FileReader();
    fr.onload = function () {
        let data = fr.result;
        sourceText.value = data;
        sourceOutput.value = "";
    }
    fr.readAsText(this.files[0]);
});