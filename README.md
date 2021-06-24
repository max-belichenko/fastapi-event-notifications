# fastapi-event-notifications
Tiny service that allow users to get event notifications from external systems.

Создать сервис уведомлений, который:
1. Принимает события от различных внешних систем по API
2. Оптравляет уведомления о событиях пользователям по e-mail

При этом:
* Можно запланировать рассылку события на определённую дату
* Рассылка производится в рабочее время относительно таймзоны пользователя

Дополнительно:
+ При реализации желательно использовать Dramatiq
