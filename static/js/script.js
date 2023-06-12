const form = document.querySelector('form');
const container = document.querySelector('.container');

// Обработчик события отправки формы
form.addEventListener('submit', function(event) {
  // Предотвращаем стандартное поведение отправки формы
  event.preventDefault();

  // Получаем данные формы
  const formData = new FormData(form);
  const url = formData.get("url")

  // Формируем строку запроса с закодированным URL
  const queryString = "/url=" + fixedEncodeURIComponent(url);

  // Отправляем запрос AJAX, используя полученные данные формы.
  fetch(queryString, {
    method: "POST",
    body: formData,
  })
  .then(response => {
      // Проверяем статус ответа
      if (!response.ok) {
        throw new Error("Ошибка при выполнении запроса");
      }
      // Преобразуем ответ в формат JSON
      return response.json();
    })
  .then(data => {
    // Получаем сокращенный URL из ответа сервера
    const shortUrl = data.shorten_url;

    // Получаем элементы DOM для отображения результата
    let resultElement = document.querySelector("#short-url");
    let resultTextElement = document.querySelector("#result");

    // Если элемент результата не существует, создаем его
    if (!resultElement) {
      resultElement = document.createElement("span");
      resultElement.id = "short-url";
      document.body.appendChild(resultElement);
    }

    // Устанавливаем текст результата
    resultTextElement.textContent = "Short URL: ";
    resultElement.textContent = shortUrl;

    // Копируем сокращенный URL в буфер обмена при клике на элемент
    resultElement.addEventListener('click', function() {
        navigator.clipboard.writeText(shortUrl)
          .then(() => {
            console.log("URL скопирован в буфер обмена");
          })
          .catch(error => {
            console.log("Ошибка при копировании URL в буфер обмена:", error);
          });
      });
  })
  .catch(error => {
    console.log("Произошла ошибка при выполнении запроса:", error);
  });
});

// Заменяет все символы, которые не допустимы в URI, на их коды в формате %XY
// где XY - это шестнадцатеричное представление кода символа
function fixedEncodeURIComponent (str) {
  return encodeURIComponent(str).replace(/[!'()*/]/g, function(c) {
    return '%' + c.charCodeAt(0).toString(16);
  });
}
