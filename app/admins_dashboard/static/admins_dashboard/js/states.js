class BaseListState {
    /*
    Базовый класс для стейтов
    */
    constructor(name, container) {
        /*
        Контруктор.
        :param name: Название стейта.
        :param container: Контейнер для списка.
        */
        this.name = name;
        this.container = container;
        this.api_root = document.querySelector('meta[name="api_root"]').content
        this.endpoints = ''
    };

    _getItemElement(itemData) {
        // Вернуть DOM-элемент для элемента списка
    }

    _getListElement(listData) {
        // Вернуть DOM-элемент для списка
    }

    _renderItems() {
        // Отрендерить список
    }

    refreshItems() {
        // Обновить список
    }

    loadItems() {
        // Загрузить объекты.
    }


}


class CompaniesState extends BaseListState {
    constructor(name) {
        super(name);
        this.endpoint = '/companies/'
    }
}