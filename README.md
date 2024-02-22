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
   1. CVE-2023-52425 - Неконтроллируемое потребление ресурсов - Продукт не контролирует должным образом распределение и обслуживание ограниченного ресурса, тем самым позволяя субъекту влиять на количество потребляемых ресурсов, что в конечном итоге приводит к исчерпанию доступных ресурсов.

      Решение: уязвимость существует до версии 2.5.0, необходимо использовать библиотеку, начиная с версии 2.6.0
   2. CVE-2023-52426 - Неправильное ограничение рекурсивных ссылок на сущности в DTD (XML Entity Expansion) - Продукт использует XML-документы и позволяет определять их структуру с помощью определения типа документа (DTD), но не контролирует должным образом количество рекурсивных определений сущностей.

      Решение: уязвимость существует до версии 2.5.0, необходимо использовать библиотеку, начиная с версии 2.6.0
   

   В библиотеке pip (METADATA) найдена одна уязвимость:
   CVE-2023-5752 -Неправильная нейтрализация специальных элементов, используемых в команде (внедрение в команду) - Продукт полностью или частично создает команду, используя входные данные вышестоящего компонента, но не нейтрализует или неправильно нейтрализует специальные элементы, которые могут изменить предполагаемую команду при ее отправке нижестоящему компоненту.

   Решение: уязвимость существует до версии 23.3, необходимо использовать библиотеку, начиная с версии 23.3. У нас ипользуется версия 23.0.1

6. В отдельную папку склонируем репозиторий утилиты bench-security
   ![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/682157ac-daa3-4ec0-a867-dd4e37762d75)

   ![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/e0baa5f2-c61b-4d5c-9a2f-7c10f94e8bdc)

   Запустим ее

   ![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/ce661708-d6a6-4998-a6ec-265d6a2267a5)
   ![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/dd9415e5-656e-41f5-ac09-264f4ac1ed23)
   ![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/1f192a8a-90d3-4aa0-9655-1d0dcaeb37ac)
   ![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/c9957a71-df54-4663-ad0c-125e25293455)
   ![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/c4b9b874-9ab9-4420-8dfe-6cc91e756b60)
   ![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/4731c784-2f40-46d3-8aee-a653a520b002)

   Получим следующие варны:
   
   1.1.1 - Ensure a separate partition for containers has been created (Automated) - Убедитесь, что создан отдельный раздел для контейнеров (автоматизирован)

   Всегда рекомендуется использовать другой, кроме раздела docker по умолчанию. Большинство облачных платформ, таких как AWS или DigitalOcean, по умолчанию никогда не предоставляют максимальное свободное место под разделом /var.       Так что в этом случае вы можете столкнуться с нехваткой дискового пространства. 

   Как найти раздел по умолчанию для контейнеров Docker? -> docker info -f'{{.DockerRootDir }}'

   
   1.1.3 - Ensure auditing is configured for the Docker daemon (Automated) - Убедитесь, что аудит настроен для демона Docker (автоматизирован)

   
   Аудит на linux-сервере может заключаться в настройке демона auditd. Этот демон отвечает за запись записи аудита в файл журнала аудита. Чтобы настроить аудит для файлов Docker, выполните:


   ![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/ba844651-decd-414e-888f-1aaeb08c16de)



   1.1.4 - Ensure auditing is configured for Docker files and directories -/run/containerd (Automated) - Убедитесь, что аудит настроен для файлов и каталогов Docker -/run/containerd (автоматический)


   Docker рекомендует использовать аудит на системном уровне для ключевых каталогов Docker. Аудит регистрирует все операции, влияющие на отслеживаемые файлы и каталоги. Это позволяет отслеживать потенциально деструктивные изменения. Убедитесь, что у вас установлен auditd. Отредактируйте файл /etc/audit/audit.rules и добавьте следующие строки в нижнюю часть файла:


![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/f9826506-1701-4899-987a-f927fcd8d700)


Инструкция -p wa означает, что auditd будет регистрировать записи и изменения атрибутов, которые влияют на файлы. Если выходные данные Docker Bench предлагают использовать аудит для дополнительных каталогов, добавьте их в список. Каталоги Docker могут меняться со временем.

Чтобы изменения вступили в силу, необходимо перезапустить auditd:

sudo systemctl restart auditd
      
   
   2.2 - Ensure network traffic is restricted between containers on the default bridge (Scored) - Убедитесь, что сетевой трафик ограничен между контейнерами на мосту по умолчанию (оценено) (файл конфигурации /etc/docker/daemon.json:
"icc":false — отключает обмен данными между контейнерами, чтобы избежать ненужной утечки информации.)
   2.9 - Enable user namespace support (Scored) - Включить поддержку пользовательского пространства имен (оценено)
   2.12 - Ensure that authorization for Docker client commands is enabled (Scored) - Убедитесь, что авторизация для клиентских команд Docker включена (оценена)
   2.13 - Ensure centralized and remote logging is configured (Scored) - Убедитесь, что настроено централизованное и удаленное ведение журнала (оценено)
   2.14 - Ensure containers are restricted from acquiring new privileges (Scored) - Убедитесь, что контейнерам запрещено получать новые привилегии (оценено)
   2.15 - Ensure live restore is enabled (Scored) - Убедитесь, что включено оперативное восстановление (оценено)
   2.16 - Ensure Userland Proxy is Disabled (Scored) - Убедитесь, что пользовательский прокси отключен (оценено)
   4.5 - Ensure Content trust for Docker is Enabled (Automated) - Убедитесь, что доверие к контенту для Docker включено (автоматически)
   4.6 - Ensure that HEALTHCHECK instructions have been added to container images (Automated) - Убедитесь, что инструкции по проверке работоспособности были добавлены к изображениям контейнеров (были добавлены до проверки)

8. Проверим уязвимости с помощью docker-scout. Для этого выберем образ и выполним анализ
   ![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/09526929-f31e-4667-afac-06cbb5365964)
   ![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/4b842547-867b-4220-980f-9e2a8527b1e2)

   В результате будут обнаружены те же самые уязвимости, что выявила утилита trivy
   ![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/eb1a2175-79e5-47b9-ab41-9049d605d4bd)
   ![image](https://github.com/egorvozhzhov/docker-test/assets/71019753/ce1e7e81-4d56-4814-b20b-25578824d331)




