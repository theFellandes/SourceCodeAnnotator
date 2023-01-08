let chooseFileButton = document.querySelector("#fileUpload");
let sourceOutput = document.querySelector("#sourceOutput");
let sourceText = document.querySelector("#sourceText");
let lazyDocButton = document.querySelector("#lazyDocButton");
let downloadButton = document.querySelector("#downloadButton");
let inputForm = document.querySelector("#inputForm");
let outputForm = document.querySelector("#outputForm");
let chad = document.querySelector("#chad");

lazyDocButton.addEventListener("click", function () {
    inputForm.action = "/lazydoc";
    inputForm.submit();
});

downloadButton.addEventListener("click", function () {
    outputForm.submit();
});

chad.addEventListener("click", function () {
    inputForm.action = "/openai";
    inputForm.submit();
})

chooseFileButton.addEventListener("change", function () {
    let fr = new FileReader();
    fr.onload = function () {
        let data = fr.result;
        sourceText.value = data;
        sourceOutput.value = "";
    }
    fr.readAsText(this.files[0]);
});