export class HttpError extends Error {
    constructor(message) {
        super(message);
        this.name = "HttpError";
    }
}


export class ServerError extends HttpError {
    constructor(error) {
        super('Сервер вернул ошибку! Повторите попытку чуть позже...');
        this.name = "ServerError";
        this.error = error;
    }
}


export class RequestError extends HttpError {
    constructor(error) {
        super('Упс! Возникла ошибка, возможно, нет соединения с интернетом...');
        this.name = "RequestError";
        this.error = error;
    }
}


export class SettingRequestError extends HttpError {
    constructor(error) {
        super('Упс! Возникла какая то ошибка, повторите попытку чуть позже...');
        this.name = "SettingRequestError";
        this.error = error;
    }
}


export function processError(error) {
	// Принимает объект ошибки и выбрасывает нужное исключение
	if (error.response) {
		throw ServerError(error)
	} else if (error.request) {
		throw RequestError(error)
	} else {
		throw SettingRequestError(error)
	}
}
