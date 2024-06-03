# helpers_entity
Helper entities for other applications

## Содержит следующие сущности:
### helpers.work_classes:
* LogConf - класс описывающий конфигурацию логирования 
* LogLevel - enum класс описывающий уровни логирования
* LogFormat - enum класс описывающий формат логов
* LogOutput - enum класс описывающий куда выводить логи
* PgConf - класс описывающий конфигурацию подключения к БД PostgreSQL
* TgBotConf - класс описывающий конфигурацию подключения к телеграм боту
* AppConf - класс описывающий конфигурацию приложения
* MinioClientConf - класс описывающий конфигурацию клиентского подключения к s3-minio
* ReturnEntity - класс описывающий сущность возвращаемую функциями
### helpers.configuration:
* log_conf - функция возвращающая класс helpers.work_classes.LogConf
* logger - сконфигурированный логгер
* pg_conf - функция возвращающая класс helpers.work_classes.PgConf
* app_conf - функция возвращающая класс helpers.work_classes.AppConf
* minio_conf - функция возвращающая класс helpers.work_classes.MinioClientConf

## Unit tests:
* Для запуска выполнить команду из директории с проектом:
  ```shell
  docker compose -f docker-compose.yaml -f composes/unit-tests.yaml up -d
  ```
* Для остановки выполнить команду из директории с проектом:
  ```shell
  docker compose -f docker-compose.yaml -f composes/unit-tests.yaml down --rmi local -v; sudo rm -f tests/reports/unit-tests.log
  ```
[Отчет](./tests/reports/unit-tests.html)

## Очистка системы после запуска тестов
Т.к. тесты и окружение разработчика построены на сборке контейнеров через compose, docker сохраняет кеш собранных
образов.
```
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          3         0         1.051GB   1.051GB (100%)
Containers      0         0         0B        0B
Local Volumes   0         0         0B        0B
Build Cache     35        0         31.73MB   31.73MB
```
* Для просмотра занимаемого места сущностями docker необходимо выполнить команду в терминале:
    ```shell
    docker system df
    ```
* Для очистки Build Cache необходимо выполнить команду в терминале:
    ```shell
    docker buildx prune -f
    ```
> [!TIP]
> Ссылка на статью с описанием функций очистки системы docker: https://depot.dev/blog/docker-clear-cache