1. Настроим docker-compose файл, в котором в качестве сервисов будет: БД redis и task. Настроим постоянное хранение, сетевое окружение и healthckecks. Для task настроим Dockerfile с необходимой версией питона (облегченной) и необходимыми библиотеками.
Также сделаем dockerignore файл для исключения Dockerfile из сборки. В app.py находится логика приложения: при помощи Flask будет подниматься сервер, из redis будем получать ФИО, формировать HTML страницу для возврата.
2. Сделаем сборку task
   
   ![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/db5d2afb-49bf-4e46-b8b2-be618a6cc223)
4. С помощью команды docker-compose up -d развернем сервисы (флаг -d выполняет команду в фоновом режиме, позволяя сохранить возможность управления терминалом). В браузере по адресу localhost:5001 увидим результат

   ![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/ca80f44a-9261-461a-b76a-26fc037371b2)

5. Перейдем к анализу безопасности. Установим trivy

   ![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/7183e3b9-f70f-46bc-a4f0-7ba0e8653aa1)

   Запустим сканирование образа task. В начале произойдет загрузка БД с уязвимостями. Далее появятся найденные уязвимости.

   ![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/a2c1653a-6cb3-44cf-80ce-ee10a29b72c7)

   В библиотеке libexpat (свободная потокоориентированная библиотека парсинга XML, написанная на C) будет найдено две уязвимости:
   1. CVE-2023-52425 - Неконтроллируемое потребление ресурсов - Продукт не контролирует должным образом распределение и обслуживание ограниченного ресурса, тем самым позволяя субъекту влиять на количество потребляемых ресурсов, что в конечном итоге приводит к исчерпанию доступных ресурсов. Решение: уязвимость существует до версии 2.5.0, необходимо использовать библиотеку, начиная с версии 2.6.0
   

