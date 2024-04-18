import bpy
from CdbsModules.Logger import logger


def translate(context, text):
    localisation = bpy.context.preferences.view.language
    if localisation == 'en_US':
        return text
    l_text = cdbs_translations_dict.get(localisation).get((context, text))
    if l_text:
        return l_text
    logger('debug', f'translation for ({context}, {text}) not found')
    return text

cdbs_translations_dict = {
    'ru_RU': {
        ('cdbs', 'Component:'): 'Компонент:',
        ('cdbs', 'Modification:'): 'Модификация:',
        ('cdbs', 'Preparing for upload file...'): 'Подготовка к отправке файла...',
        ('cdbs', 'Upload file...'): 'Загрузка файла...',
        ('cdbs', 'Exception in upload file:'): 'Ошибка при загрузке файла:',
        ('cdbs', 'File uploaded. Response bytes:'): 'Файл загружен. Содержимое ответа:',
        ('cdbs', 'The path to the local library specified is missing (set in the settings).'): 'Не указан путь к локальной библиотеке (задаётся в настройках).',
        ('cdbs', 'Received data about components is not suitable for processing'): 'Полученные данные о компонентах не пригодны для обработки.',
        ('cdbs', "You don't have favorite components"): 'У пользователя нет избранных компонентов',
        ('cdbs', 'Component UUID:'): 'Идентификатор компонента (UUID):',
        ('cdbs', 'Component list update finished.'): 'Завершенно обновление списка компонентов.',
        ('cdbs', 'Not set UUID for select component.'): 'Не установлен UUID для выбранного компонента.',
        ('cdbs', 'Received data about component is not suitable for processing.'): 'Полученные данные о компоненте не подходят для обработки.',
        ('cdbs', 'No modifications for the component.'): 'У компонента нет модификаций.',
        ('cdbs', 'The list of modifications to the component has been updated.'): 'Список модификаций компонента обновлён.',
        ('cdbs', 'Not set UUID for select modification.'): 'Не установлен UUID для выбранной модификации.',
        ('cdbs', 'Received data about fileset is not suitable for processing.'): 'Полученные данные о наборе файлов не подходят для обработки.',
        ('cdbs', 'Fileset not found for Blender.'): 'Набор файлов для Blender не найден.',
        ('cdbs', 'Received data about files of fileset is not suitable for processing.'): 'Получены данные о файлах набора файлов, не пригодны для обработки.',
        ('cdbs', 'No files in fileset.'): 'В наборе файлов нет файлов.',
        ('cdbs', 'Download file(s):'): 'Скачанных файлов:',
        ('cdbs', 'The set of files for the component modification has been updated.'): 'Набор файлов модификации компонента обновлен.',
        ('cdbs', 'Please specify path to the local library in CADBase Library (addon) settings.'): 'Укажите путь к локальной библиотеке в настройках библиотеки CADBase (аддона).',
        ('cdbs', 'Need set correct settings:'): 'Необходимо установить правильные настройки:',
        ('cdbs', 'Successful authorization.'): 'Успешная авторизация.',
        ('cdbs', 'Failed authorization.'): 'Ошибка при авторизации.',
        ('cdbs', 'API Point:'): 'Адрес сервера:',
        ('cdbs', 'Getting a new token, please wait.'): 'Получение нового токена, пожалуйста, подождите.',
        ('cdbs', 'Exception when trying to login:'): 'Ошибка при попытке авторизироваться:',
        ('cdbs', 'Need reset a point.'): 'Необходимо сбросить точку.',
        ('cdbs', 'Resetting the end point.'): 'Сброс конечной точки завершен.',
        ('cdbs', 'Updating settings.'): 'Обновление настроек.',
        ('cdbs', 'No changes found.'): 'Изменений не обнаружено.',
        ('cdbs', 'The path to the library in the local repository has been updated.'): 'Путь к библиотеке в локальном хранилище был обновлен.',
        ('cdbs', 'Success.'): 'Успех.',
        ('cdbs', 'Failed, status code:'): 'Не удалось, код состояния:',
        ('cdbs', 'File already exists and skipped:'): 'Файл уже существует и пропущен:',
        ('cdbs', 'Exception in download file:'): 'Исключение при скачивании файла:',
        ('cdbs', 'Error:'): 'Ошибка:',
        ('cdbs', 'path:'): 'путь:',
        ('cdbs', 'time:'): 'время:',
        ('cdbs', 'sec'): 'сек',
        ('cdbs', 'Total time:'): 'Общее время:',
        ('cdbs', 'Data processing, please wait.'): 'Обработка данных, пожалуйста, подождите.',
        ('cdbs', 'Not found file with response.'): 'Не найден файл с ответом.',
        ('cdbs', 'There was an error with response processing.'): 'При обработке ответа произошла ошибка.',
        ('cdbs', 'Exception occurred while parsing the server response:'): 'При разборе ответа сервера возникло исключение:',
        ('cdbs', 'No data found to delete.'): 'Не найдено данных для удаления.',
        ('cdbs', 'Exception occurred while trying to save old response:'): 'При попытке сохранить старый ответ возникло исключение:',
        ('cdbs', 'removed'): 'удалён',
        ('cdbs', 'Please delete this file for correct operation:'): 'Пожалуйста, удалите этот файл для корректной работы:',
        ('cdbs', 'Exception occurred while trying to write the file:'): 'При попытке записать файл возникло исключение:',
        ('cdbs', 'Selected'): 'Выбран',
        ('cdbs', 'Exception when trying to read information from the file:'): 'Исключение при попытке прочитать информацию из файла:',
        ('cdbs', 'Failed to parse GraphQL before deep parsing:'): 'Не удалось разобрать GraphQL перед глубоким разбором:',
        ('cdbs', 'Received data is not suitable for processing about'): 'Полученные данные не подходят для обработки о',
        ('cdbs', 'Structure data:'): 'Данные структуры:',
        ('cdbs', 'Not found data for UUID selection:'): 'Данные для определения UUID не найдены:',
        ('cdbs', 'Structure vars:'): 'Структурные переменные:',
        ('cdbs', 'UUID of structure data:'): 'UUID данных структуры:',
        ('cdbs', 'Preparing for uploading files...'): 'Подготовка к выгрузке файлов...',
        ('cdbs', 'To upload files, you must select the modification folder.'): 'Чтобы загрузить файлы, необходимо выбрать папку модификации.',
        ('cdbs', 'Modification UUID:'): 'UUID модификации:',
        ('cdbs', 'To send files to CADBase, you must open the modification or file set folder.'): 'Чтобы отправить файлы в CADBase, необходимо открыть папку модификации или набора файлов.',
        ('cdbs', 'Files in the CADBase storage have been updated successfully.'): 'Файлы в хранилище CADBase были успешно обновлены.',
        ('cdbs', 'Getting fileset UUID...'): 'Получение UUID набора файлов...',
        ('cdbs', 'Fileset UUID:'): 'UUID набора файлов:',
        ('cdbs', 'Creating a new set of files for Blender.'): 'Создание нового набора файлов для Blender.',
        ('cdbs', 'Error occurred while getting the UUID of the file set.'): 'Возникла ошибка при получении UUID набора файлов.',
        ('cdbs', 'Error occurred while confirming the upload of files, \
the files were not uploaded to correctly.'): 'Возникла ошибка при подтверждении загрузки файлов, файлы были загружены неправильно.',
        ('cdbs', 'No files found for upload.'): 'Не найдено ни одного файла для загрузки.',
        ('cdbs', 'Success upload files to CADBase storage:'): 'Успешная загрузка файлов в хранилище CADBase:',
        ('cdbs', 'Last clicked dir:'): 'Последний клик по директории:',
        ('cdbs', 'Local files:'): 'Локальные файлы:',
        ('cdbs', 'Cloud filenames:'): 'Имена облачных файлов:',
        ('cdbs', 'The local file has a cloud version:'): 'Локальный файл имеет облачную версию:',
        ('cdbs', 'Local file does not have a cloud version:'): 'Локальный файл не имеет облачной версии:',
        ('cdbs', 'New files to upload:'): 'Новые файлы для загрузки:',
        ('cdbs', 'Blake3 import error:'): 'Ошибка импорта Blake3:',
        ('cdbs', 'For compare hashes need install `blake3`. \
Please try to install it with: `pip install blake3` or some other way.'): 'Для сравнения хэшей необходимо установить `blake3`. \
Пожалуйста, попробуйте установить его с помощью: `pip install blake3` или другим способом.',
        ('cdbs', 'File hash from CADBase not found, this file is skipped:'): 'Хеш файла из CADBase не найден, этот файл пропущен:',
        ('cdbs', 'Found not file and it skipped'): 'Не найден файл, пропущен',
        ('cdbs', 'Error calculating hash for local file'): 'Ошибка при вычислении хэша для локального файла.',
        ('cdbs', 'File hash'): 'Хеш файла',
        ('cdbs', 'local'): 'локально',
        ('cdbs', 'cloud'): 'в облаке',
        ('cdbs', 'Selected files to upload:'): 'Выбранные файлы для загрузки:',
        ('cdbs', 'Uploading files to cloud storage (this can take a long time).'): 'Загрузка файлов в облачное хранилище (это может занять много времени).',
        ('cdbs', 'Failed to upload files.'): 'Не удалось загрузить файлы.',
        ('cdbs', 'Confirmation of successful files upload:'): 'Подтверждение успешной загрузки файлов:',
        ('cdbs', 'Completed upload:'): 'Загрузка завершена:',
        ('cdbs', 'Filename:'): 'Имя файла:',
        ('cdbs', 'For correct operation of the addon it is necessary to free the path \
or change the location of the local library. Path:'): 'Для корректной работы аддона необходимо освободить путь или изменить расположение локальной библиотеки. Путь:',
        ('cdbs', 'Successful processing request.'): 'Успешная обработка запроса.',
        ('cdbs', 'Failed processing request.'): 'Не удалось обработать запрос.',
        ('cdbs', 'Token not found. Please get a new token and try again.'): 'Токен не найден. Пожалуйста, получите новый токен и повторите попытку.',
        ('cdbs', 'Getting data...'): 'Получение данных...',
        ('cdbs', 'Query include body:'): 'Запрос включает тело:',
        ('cdbs', 'Exception when trying to sending the request:'): 'Исключение при попытке отправить запрос:',
        ('cdbs', 'Configuration updated.'): 'Конфигурация обновлена.',
        ('cdbs', 'No changes.'): 'Изменений нет.',
        ('cdbs', 'Target list not found.'): 'Список целей не найден.',
        ('cdbs', 'Target index not found:'): 'Целевой индекс не найден:',
        ('cdbs', 'Need open modification, now:'): 'Нужна открытая модификация, срочно:',
        ('cdbs', "You can't create a link to a file because it's already open."): 'Нельзя создать ссылку на файл, потому что он уже открыт.',
        ('cdbs', 'Skip (file path does not exist):'): 'Пропуск (файла не существует):',
        ('cdbs', 'Skip:'): 'Пропущен:',
        ('cdbs', 'Skip object:'): 'Пропущен объект:',
        ('cdbs', 'Failed with get path:'): 'Не удалось получить путь:',
        ('cdbs', 'The target path is not a directory.'): 'Целевой путь не является каталогом.',
        ('cdbs', 'Failed to determine the type of the open object:'): 'Не удалось определить тип открытого объекта:'
    }
}

translations_dict = {
    'ru_RU': {
        ('*', 'CADBase Library'): 'Библиотека CADBase',
        ('*', 'This is add-on for synchronizing data with CADBase cloud storage'): 'Этот аддон предназначен для синхронизации данных с облачным хранилищем CADBase',
        ('*', 'Components (parts)'): 'Компоненты (детали)',
        ('*', 'Library path'): 'Путь к библиотеке',
        ('*', 'The addon will use this directory '): 'Аддон будет использовать этот каталог ',
        ('*', 'to save downloaded files. Be careful, '): 'для сохранения загруженных файлов. Будьте осторожны, ',
        ('*', 'data in this directory may be overwritten.'): 'данные в этой директории могут быть перезаписаны.',
        ('*', 'Point API'): 'Point API',
        ('*', 'Here you can specify the server on which '): 'Здесь указывается сервер, на котором ',
        ('*', 'the CADBase platform. Specify the server '): 'платформа CADBase. Укажите сервер ',
        ('*', '(URL or IP) if you need to connect to the '): '(URL или IP), если нужно подключиться к ',
        ('*', 'unofficial CADBase platform server.'): 'неофициальному серверу платформы CADBase.',
        ('*', 'Authorization'): 'Авторизация',
        ('*', 'CADBase platform access token will be saved locally,'): 'Токен доступа к платформе CADBase будет сохранен локально,',
        ('*', 'after successful authorization. When the authorization '): 'после успешной авторизации. Когда срок действия маркера ',
        ('*', 'token expires, you will need to request a new '): 'токен истекает, необходимо запросить новый ',
        ('*', 'authorization token by re-entering your username '): 'запросить новый токен авторизации, повторно введя свое имя пользователя ',
        ('*', 'and password.'): 'и пароль.',
        ('*', 'Username'): 'Имя пользователя',
        ('*', 'Password'): 'Пароль',
        ('Operator', 'CADBase Library Configuration'): 'Библиотека CADBase - Конфигурация',
        ('Operator', 'CADBase Library Authorization'): 'Библиотека CADBase - Авторизация',
        ('Operator', 'Open'): 'Открыть',
        ('Operator', 'Go back'): 'Назад',
        ('Operator', 'Authorization'): 'Авторизация',
        ('Operator', 'Pull data'): 'Получить данные',
        ('Operator', 'Link file'): 'Прилинковать файл',
        ('Operator', 'Push changes'): 'Отправить изменения',
        ('Operator', 'Settings'): 'Настройки',
        ('Operator', 'Reset API point'): 'Сброс адреса сервера',
        ('Operator', 'Sets the selected folder as the current position and updates the list'): 'Устанавливает выбранную папку в качестве текущей позиции и обновляет список',
        ('Operator', 'Sets the parent folder to active and updates the list'): 'Устанавливает родительскую папку активной и обновляет список',
        ('Operator', 'Retrieves data from cloud storage and updates the list'): 'Получает данные из облачного хранилища и обновляет список',
        ('Operator', 'Creates a reference to objects in the target file'): 'Создает ссылку на объекты в целевом файле',
        ('Operator', 'Starts the process of sending changes from local storage to the cloud.'): 'Запускает процесс отправки изменений из локального хранилища в облако.',
        ('Operator', 'Opens the tool (addon) settings in a separate window'): 'Открывает настройки инструмента (аддона) в отдельном окне',
        ('Operator', 'Opens the window of authorization and updating the access token to CADBase platform'): 'Открывает окно авторизации и обновления токена доступа к платформе CADBase',
        ('Operator', 'Sets as value the API point of the main CADBase platform server'): 'Устанавливает в качестве значения точку API основного сервера платформы CADBase',
        ('Operator', 'The selected directory will store data about components, modifications and file sets.'): 'В выбранном каталоге будут храниться данные о компонентах, модификациях и наборах файлов.'
    }
}