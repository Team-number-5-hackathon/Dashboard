import './LayoutDocs.css';
import '../../globals.css'

function LayoutDocs() {

    return (
        <section id='docs' className='docs'>
            <div className="docs__column">
                <h1 className="docs__header">Описание дашборда</h1>
                <p className="column__text">Текст документации в первом столбце</p>

                <h1 className="docs__header">Метрики</h1>
                <p className="column__text">Количество уникальных сотрудников SELECT COUNT(DISTINCT ID) FROM df;
                    Средний балл SELECT AVG(оценка_) FROM df;
                    Количество уникальных навыков SELECT COUNT(DISTINCT навык) FROM df;</p>
            </div>
            <div className="docs__column">
                <h1 className="docs__header">Описание датасета</h1>
                <p className="column__text">
                    1. ID: Уникальный идентификационный номер сотрудника.<br/>
                    2. Сотрудник: Полное имя сотрудника, представленное в формате ФИО (Фамилия, Имя, Отчество).<br/>
                    3. Должность: Должность, занимаемая сотрудником в организации.
                    4. Команда: Название команды, в которой работает сотрудник.<br/>
                    5. Грейд: Уровень профессионального развития сотрудника, который может принимать одно из следующих
                    значений: Junior, Middle, Senior.<br/>
                    6. Создан: Дата создания записи о сотруднике в системе.<br/>
                    7. Навык: Название конкретного навыка, который оценивается у сотрудника.<br/>
                    8. Компетенция: Группа навыков, объединённых по общей тематике.<br/>
                    9. Домен: Обобщённая категория, классифицирующая навыки на две основные группы: "хард-скиллы" и
                    "софт-скиллы".<br/>
                    10. Дата: Дата проведения экзаменации или оценки навыков сотрудника.<br/>
                    11. Оценка_: Числовая оценка, представляющая уровень владения навыком по пятибалльной системе:<br/>
                    &#8226; 1 — не владеет,
                    &#8226; 2 — начинающий,
                    &#8226; 3 — базовый,
                    &#8226; 4 — уверенный,
                    &#8226; 5 — экспертный.
                    1. Оценка: Строковое представление числовой оценки навыка из столбца "Оценка_".<br/>
                    2. Соответствие: Показатель, отражающий, соответствует ли уровень владения навыком установленному
                    уровню для данного сотрудника</p>
            </div>

        </section>
    );
}

export default LayoutDocs;