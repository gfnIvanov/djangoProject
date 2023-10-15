document.addEventListener("DOMContentLoaded", () => {
    const selectList = document.getElementById('lang-select');
    selectList.value = 'ru';
});

const BASE_ELEMENTS_TEXT = {
    en: {
        'main-page-btn': 'Main',
        'articles-page-btn': 'Articles',
        'practice-page-btn': 'Practice',
        'reg-btn': 'Registration',
        'log-in-btn': 'Log In',
        'log-out-btn': 'Log out',
        'language-label': 'Page language'
    },
    ru: {
        'main-page-btn': 'Главная',
        'articles-page-btn': 'Статьи',
        'practice-page-btn': 'Практика',
        'reg-btn': 'Регистрация',
        'log-in-btn': 'Вход',
        'log-out-btn': 'Выход',
        'language-label': 'Язык страницы'
    }
};

const BASE_ELEMENTS_IDS = [
    'main-page-btn',
    'articles-page-btn',
    'practice-page-btn',
    'reg-page-btn',
    'log-in-btn',
    'log-out-btn',
    'language-label'
];

const translatePage = async function(select) {
    const lang = select.value;
    const translateToLang = translateElement.bind(null, lang);
    const activePage = document.getElementById('active_page').innerText;
    BASE_ELEMENTS_IDS.forEach(id => {
        try {
            const element = document.getElementById(id);
            element.innerText = BASE_ELEMENTS_TEXT[lang][id];
        } catch(e) {
            return;
        }
    });
    if (activePage === 'index') {
        await translateToLang('main-page-title');
        await translateToLang('main-page-content');
    }
};

const translateElement = async function(lang, id) {
    const element = document.getElementById(id);
    const response = await fetch(`https://functions.yandexcloud.net/d4en4qqq9eu1tpvhr0eb?target=${lang}&text=${element.innerText}`, {
        method: 'POST'
    });
    const result = await response.json()
    const newText = JSON.parse(result.result).translations.map(tr => tr.text).join(' ');
    element.innerText = newText;
};
