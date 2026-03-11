window.onload = function () {
  const inputDivs = document.getElementsByClassName("input_div");
  for (let div of inputDivs) div.style.display = "none";
};

document.getElementById("input_type").addEventListener("change", function () {
  const selectedInput = this.value;
  const inputDivs = document.getElementsByClassName("input_div");
  for (let div of inputDivs) div.style.display = "none";

  if (selectedInput === "microphone")
    document.getElementById("microphone_input").style.display = "block";
  if (selectedInput === "audio_file")
    document.getElementById("audio_file_input").style.display = "block";
  if (selectedInput === "video_file")
    document.getElementById("video_file_input").style.display = "block";
});

$("form").on("submit", function () {
  $("#loading-screen").show();
});

$(document).ajaxComplete(function () {
  $("#loading-screen").hide();
});
