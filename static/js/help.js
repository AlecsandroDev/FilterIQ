document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("btn_talk").addEventListener("click", function () {
    axios
      .get("https://filteriq.onrender.com/talk")
      .then(function (response) {
        window.location.href = 'https://filteriq.onrender.com/talk';
      })
      .catch(function (error) {
        console.log("Erro na requisição:", error)
      })
  })
});
