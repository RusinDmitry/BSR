# Интеллектуальная система прогнозирования заболевания инфаркта миокарда

Программная система с возможностью прогнозирования течения болезни пациента и выявления рекомендаций по лечению

___
## Набор данных
База данных содержит информацию о течении заболевания у 1700 больных с инфарктом миокарда

Информация получена из историй болезни пациентов и содержит сведения: 
- личные данные больного (пол, возраст);
- анамнез больного;
- клиника настоящего инфаркта миокарда; 
- электрокардиографические показатели; 
- лабораторные показатели;
- лекарственная терапия;
- особенности течения заболевания в первые дни инфаркта миокарда;

## Структура

- В папке CardioAI расположен непосредственно сам сервис с веб-интерфейсом
Для запуска сервиса необходимо запустить файл


    run.py

- В папке Scripts расположены notebooks с обработкой исходных данных и экспериментальным обучением разных моделей, плюс сохраненные модели под каждое осложнение

## Требования
Сервису необходимы следующие пакеты:
- python (3.8>);
- numpy;
- pandas;
- tensorflow;
- sklearn;
- catboost;
- joblib;
- dash;