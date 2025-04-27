(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_translation_lib_index_js"],{

/***/ "../packages/translation/lib/base.js":
/*!*******************************************!*\
  !*** ../packages/translation/lib/base.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "nullTranslator": () => (/* binding */ nullTranslator)
/* harmony export */ });
/* harmony import */ var _gettext__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./gettext */ "../packages/translation/lib/gettext.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

/**
 * A translator that loads a dummy language bundle that returns the same input
 * strings.
 */
class NullTranslator {
    constructor(bundle) {
        this._languageBundle = bundle;
    }
    load(domain) {
        return this._languageBundle;
    }
    locale() {
        return 'en';
    }
}
/**
 * A language bundle that returns the same input strings.
 */
class NullLanguageBundle {
    __(msgid, ...args) {
        return this.gettext(msgid, ...args);
    }
    _n(msgid, msgid_plural, n, ...args) {
        return this.ngettext(msgid, msgid_plural, n, ...args);
    }
    _p(msgctxt, msgid, ...args) {
        return this.pgettext(msgctxt, msgid, ...args);
    }
    _np(msgctxt, msgid, msgid_plural, n, ...args) {
        return this.npgettext(msgctxt, msgid, msgid_plural, n, ...args);
    }
    gettext(msgid, ...args) {
        return _gettext__WEBPACK_IMPORTED_MODULE_0__.Gettext.strfmt(msgid, ...args);
    }
    ngettext(msgid, msgid_plural, n, ...args) {
        return _gettext__WEBPACK_IMPORTED_MODULE_0__.Gettext.strfmt(n == 1 ? msgid : msgid_plural, ...[n].concat(args));
    }
    pgettext(msgctxt, msgid, ...args) {
        return _gettext__WEBPACK_IMPORTED_MODULE_0__.Gettext.strfmt(msgid, ...args);
    }
    npgettext(msgctxt, msgid, msgid_plural, n, ...args) {
        return this.ngettext(msgid, msgid_plural, n, ...args);
    }
    dcnpgettext(domain, msgctxt, msgid, msgid_plural, n, ...args) {
        return this.ngettext(msgid, msgid_plural, n, ...args);
    }
}
/**
 * The application null translator instance that just returns the same text.
 * Also provides interpolation.
 */
const nullTranslator = new NullTranslator(new NullLanguageBundle());


/***/ }),

/***/ "../packages/translation/lib/gettext.js":
/*!**********************************************!*\
  !*** ../packages/translation/lib/gettext.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Gettext": () => (/* binding */ Gettext)
/* harmony export */ });
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./utils */ "../packages/translation/lib/utils.js");
/* ----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|
| Base gettext.js implementation.
| Copyright (c) Guillaume Potier.
| Distributed under the terms of the Modified MIT License.
| See: https://github.com/guillaumepotier/gettext.js
|
| Type definitions.
| Copyright (c) Julien Crouzet and Florian Schwingenschlögl.
| Distributed under the terms of the Modified MIT License.
| See: https://github.com/DefinitelyTyped/DefinitelyTyped
|----------------------------------------------------------------------------*/

/**
 * Gettext class providing localization methods.
 */
class Gettext {
    constructor(options) {
        options = options || {};
        // default values that could be overridden in Gettext() constructor
        this._defaults = {
            domain: 'messages',
            locale: document.documentElement.getAttribute('lang') || 'en',
            pluralFunc: function (n) {
                return { nplurals: 2, plural: n != 1 ? 1 : 0 };
            },
            contextDelimiter: String.fromCharCode(4),
            stringsPrefix: ''
        };
        // Ensure the correct separator is used
        this._locale = (options.locale || this._defaults.locale).replace('_', '-');
        this._domain = (0,_utils__WEBPACK_IMPORTED_MODULE_0__.normalizeDomain)(options.domain || this._defaults.domain);
        this._contextDelimiter =
            options.contextDelimiter || this._defaults.contextDelimiter;
        this._stringsPrefix = options.stringsPrefix || this._defaults.stringsPrefix;
        this._pluralFuncs = {};
        this._dictionary = {};
        this._pluralForms = {};
        if (options.messages) {
            this._dictionary[this._domain] = {};
            this._dictionary[this._domain][this._locale] = options.messages;
        }
        if (options.pluralForms) {
            this._pluralForms[this._locale] = options.pluralForms;
        }
    }
    /**
     * Set current context delimiter.
     *
     * @param delimiter - The delimiter to set.
     */
    setContextDelimiter(delimiter) {
        this._contextDelimiter = delimiter;
    }
    /**
     * Get current context delimiter.
     *
     * @return The current delimiter.
     */
    getContextDelimiter() {
        return this._contextDelimiter;
    }
    /**
     * Set current locale.
     *
     * @param locale - The locale to set.
     */
    setLocale(locale) {
        this._locale = locale.replace('_', '-');
    }
    /**
     * Get current locale.
     *
     * @return The current locale.
     */
    getLocale() {
        return this._locale;
    }
    /**
     * Set current domain.
     *
     * @param domain - The domain to set.
     */
    setDomain(domain) {
        this._domain = (0,_utils__WEBPACK_IMPORTED_MODULE_0__.normalizeDomain)(domain);
    }
    /**
     * Get current domain.
     *
     * @return The current domain string.
     */
    getDomain() {
        return this._domain;
    }
    /**
     * Set current strings prefix.
     *
     * @param prefix - The string prefix to set.
     */
    setStringsPrefix(prefix) {
        this._stringsPrefix = prefix;
    }
    /**
     * Get current strings prefix.
     *
     * @return The strings prefix.
     */
    getStringsPrefix() {
        return this._stringsPrefix;
    }
    /**
     * `sprintf` equivalent, takes a string and some arguments to make a
     * computed string.
     *
     * @param fmt - The string to interpolate.
     * @param args - The variables to use in interpolation.
     *
     * ### Examples
     * strfmt("%1 dogs are in %2", 7, "the kitchen"); => "7 dogs are in the kitchen"
     * strfmt("I like %1, bananas and %1", "apples"); => "I like apples, bananas and apples"
     */
    static strfmt(fmt, ...args) {
        return (fmt
            // put space after double % to prevent placeholder replacement of such matches
            .replace(/%%/g, '%% ')
            // replace placeholders
            .replace(/%(\d+)/g, function (str, p1) {
            return args[p1 - 1];
        })
            // replace double % and space with single %
            .replace(/%% /g, '%'));
    }
    /**
     * Load json translations strings (In Jed 2.x format).
     *
     * @param jsonData - The translation strings plus metadata.
     * @param domain - The translation domain, e.g. "jupyterlab".
     */
    loadJSON(jsonData, domain) {
        if (!jsonData[''] ||
            !jsonData['']['language'] ||
            !jsonData['']['pluralForms']) {
            throw new Error(`Wrong jsonData, it must have an empty key ("") with "language" and "pluralForms" information: ${jsonData}`);
        }
        domain = (0,_utils__WEBPACK_IMPORTED_MODULE_0__.normalizeDomain)(domain);
        let headers = jsonData[''];
        let jsonDataCopy = JSON.parse(JSON.stringify(jsonData));
        delete jsonDataCopy[''];
        this.setMessages(domain || this._defaults.domain, headers['language'], jsonDataCopy, headers['pluralForms']);
    }
    /**
     * Shorthand for gettext.
     *
     * @param msgid - The singular string to translate.
     * @param args - Any additional values to use with interpolation.
     *
     * @return A translated string if found, or the original string.
     *
     * ### Notes
     * This is not a private method (starts with an underscore) it is just
     * a shorter and standard way to call these methods.
     */
    __(msgid, ...args) {
        return this.gettext(msgid, ...args);
    }
    /**
     * Shorthand for ngettext.
     *
     * @param msgid - The singular string to translate.
     * @param msgid_plural - The plural string to translate.
     * @param n - The number for pluralization.
     * @param args - Any additional values to use with interpolation.
     *
     * @return A translated string if found, or the original string.
     *
     * ### Notes
     * This is not a private method (starts with an underscore) it is just
     * a shorter and standard way to call these methods.
     */
    _n(msgid, msgid_plural, n, ...args) {
        return this.ngettext(msgid, msgid_plural, n, ...args);
    }
    /**
     * Shorthand for pgettext.
     *
     * @param msgctxt - The message context.
     * @param msgid - The singular string to translate.
     * @param args - Any additional values to use with interpolation.
     *
     * @return A translated string if found, or the original string.
     *
     * ### Notes
     * This is not a private method (starts with an underscore) it is just
     * a shorter and standard way to call these methods.
     */
    _p(msgctxt, msgid, ...args) {
        return this.pgettext(msgctxt, msgid, ...args);
    }
    /**
     * Shorthand for npgettext.
     *
     * @param msgctxt - The message context.
     * @param msgid - The singular string to translate.
     * @param msgid_plural - The plural string to translate.
     * @param n - The number for pluralization.
     * @param args - Any additional values to use with interpolation.
     *
     * @return A translated string if found, or the original string.
     *
     * ### Notes
     * This is not a private method (starts with an underscore) it is just
     * a shorter and standard way to call these methods.
     */
    _np(msgctxt, msgid, msgid_plural, n, ...args) {
        return this.npgettext(msgctxt, msgid, msgid_plural, n, ...args);
    }
    /**
     * Translate a singular string with extra interpolation values.
     *
     * @param msgid - The singular string to translate.
     * @param args - Any additional values to use with interpolation.
     *
     * @return A translated string if found, or the original string.
     */
    gettext(msgid, ...args) {
        return this.dcnpgettext('', '', msgid, '', 0, ...args);
    }
    /**
     * Translate a plural string with extra interpolation values.
     *
     * @param msgid - The singular string to translate.
     * @param args - Any additional values to use with interpolation.
     *
     * @return A translated string if found, or the original string.
     */
    ngettext(msgid, msgid_plural, n, ...args) {
        return this.dcnpgettext('', '', msgid, msgid_plural, n, ...args);
    }
    /**
     * Translate a contextualized singular string with extra interpolation values.
     *
     * @param msgctxt - The message context.
     * @param msgid - The singular string to translate.
     * @param args - Any additional values to use with interpolation.
     *
     * @return A translated string if found, or the original string.
     *
     * ### Notes
     * This is not a private method (starts with an underscore) it is just
     * a shorter and standard way to call these methods.
     */
    pgettext(msgctxt, msgid, ...args) {
        return this.dcnpgettext('', msgctxt, msgid, '', 0, ...args);
    }
    /**
     * Translate a contextualized plural string with extra interpolation values.
     *
     * @param msgctxt - The message context.
     * @param msgid - The singular string to translate.
     * @param msgid_plural - The plural string to translate.
     * @param n - The number for pluralization.
     * @param args - Any additional values to use with interpolation
     *
     * @return A translated string if found, or the original string.
     */
    npgettext(msgctxt, msgid, msgid_plural, n, ...args) {
        return this.dcnpgettext('', msgctxt, msgid, msgid_plural, n, ...args);
    }
    /**
     * Translate a singular string with extra interpolation values.
     *
     * @param domain - The translations domain.
     * @param msgctxt - The message context.
     * @param msgid - The singular string to translate.
     * @param msgid_plural - The plural string to translate.
     * @param n - The number for pluralization.
     * @param args - Any additional values to use with interpolation
     *
     * @return A translated string if found, or the original string.
     */
    dcnpgettext(domain, msgctxt, msgid, msgid_plural, n, ...args) {
        domain = (0,_utils__WEBPACK_IMPORTED_MODULE_0__.normalizeDomain)(domain) || this._domain;
        let translation;
        let key = msgctxt
            ? msgctxt + this._contextDelimiter + msgid
            : msgid;
        let options = { pluralForm: false };
        let exist = false;
        let locale = this._locale;
        let locales = this.expandLocale(this._locale);
        for (let i in locales) {
            locale = locales[i];
            exist =
                this._dictionary[domain] &&
                    this._dictionary[domain][locale] &&
                    this._dictionary[domain][locale][key];
            // check condition are valid (.length)
            // because it's not possible to define both a singular and a plural form of the same msgid,
            // we need to check that the stored form is the same as the expected one.
            // if not, we'll just ignore the translation and consider it as not translated.
            if (msgid_plural) {
                exist = exist && this._dictionary[domain][locale][key].length > 1;
            }
            else {
                exist = exist && this._dictionary[domain][locale][key].length == 1;
            }
            if (exist) {
                // This ensures that a variation is used.
                options.locale = locale;
                break;
            }
        }
        if (!exist) {
            translation = [msgid];
            options.pluralFunc = this._defaults.pluralFunc;
        }
        else {
            translation = this._dictionary[domain][locale][key];
        }
        // Singular form
        if (!msgid_plural) {
            return this.t(translation, n, options, ...args);
        }
        // Plural one
        options.pluralForm = true;
        let value = exist ? translation : [msgid, msgid_plural];
        return this.t(value, n, options, ...args);
    }
    /**
     * Split a locale into parent locales. "es-CO" -> ["es-CO", "es"]
     *
     * @param locale - The locale string.
     *
     * @return An array of locales.
     */
    expandLocale(locale) {
        let locales = [locale];
        let i = locale.lastIndexOf('-');
        while (i > 0) {
            locale = locale.slice(0, i);
            locales.push(locale);
            i = locale.lastIndexOf('-');
        }
        return locales;
    }
    /**
     * Split a locale into parent locales. "es-CO" -> ["es-CO", "es"]
     *
     * @param pluralForm - Plural form string..
     * @return An function to compute plural forms.
     */
    getPluralFunc(pluralForm) {
        // Plural form string regexp
        // taken from https://github.com/Orange-OpenSource/gettext.js/blob/master/lib.gettext.js
        // plural forms list available here http://localization-guide.readthedocs.org/en/latest/l10n/pluralforms.html
        let pf_re = new RegExp('^\\s*nplurals\\s*=\\s*[0-9]+\\s*;\\s*plural\\s*=\\s*(?:\\s|[-\\?\\|&=!<>+*/%:;n0-9_()])+');
        if (!pf_re.test(pluralForm))
            throw new Error(Gettext.strfmt('The plural form "%1" is not valid', pluralForm));
        // Careful here, this is a hidden eval() equivalent..
        // Risk should be reasonable though since we test the pluralForm through regex before
        // taken from https://github.com/Orange-OpenSource/gettext.js/blob/master/lib.gettext.js
        // TODO: should test if https://github.com/soney/jsep present and use it if so
        return new Function('n', 'let plural, nplurals; ' +
            pluralForm +
            ' return { nplurals: nplurals, plural: (plural === true ? 1 : (plural ? plural : 0)) };');
    }
    /**
     * Remove the context delimiter from string.
     *
     * @param str - Translation string.
     * @return A translation string without context.
     */
    removeContext(str) {
        // if there is context, remove it
        if (str.indexOf(this._contextDelimiter) !== -1) {
            let parts = str.split(this._contextDelimiter);
            return parts[1];
        }
        return str;
    }
    /**
     * Proper translation function that handle plurals and directives.
     *
     * @param messages - List of translation strings.
     * @param n - The number for pluralization.
     * @param options - Translation options.
     * @param args - Any variables to interpolate.
     *
     * @return A translation string without context.
     *
     * ### Notes
     * Contains juicy parts of https://github.com/Orange-OpenSource/gettext.js/blob/master/lib.gettext.js
     */
    t(messages, n, options, ...args) {
        // Singular is very easy, just pass dictionary message through strfmt
        if (!options.pluralForm)
            return (this._stringsPrefix +
                Gettext.strfmt(this.removeContext(messages[0]), ...args));
        let plural;
        // if a plural func is given, use that one
        if (options.pluralFunc) {
            plural = options.pluralFunc(n);
            // if plural form never interpreted before, do it now and store it
        }
        else if (!this._pluralFuncs[options.locale || '']) {
            this._pluralFuncs[options.locale || ''] = this.getPluralFunc(this._pluralForms[options.locale || '']);
            plural = this._pluralFuncs[options.locale || ''](n);
            // we have the plural function, compute the plural result
        }
        else {
            plural = this._pluralFuncs[options.locale || ''](n);
        }
        // If there is a problem with plurals, fallback to singular one
        if ('undefined' === typeof !plural.plural ||
            plural.plural > plural.nplurals ||
            messages.length <= plural.plural)
            plural.plural = 0;
        return (this._stringsPrefix +
            Gettext.strfmt(this.removeContext(messages[plural.plural]), ...[n].concat(args)));
    }
    /**
     * Set messages after loading them.
     *
     * @param domain - The translation domain.
     * @param locale - The translation locale.
     * @param messages - List of translation strings.
     * @param pluralForms - Plural form string.
     *
     * ### Notes
     * Contains juicy parts of https://github.com/Orange-OpenSource/gettext.js/blob/master/lib.gettext.js
     */
    setMessages(domain, locale, messages, pluralForms) {
        domain = (0,_utils__WEBPACK_IMPORTED_MODULE_0__.normalizeDomain)(domain);
        if (pluralForms)
            this._pluralForms[locale] = pluralForms;
        if (!this._dictionary[domain])
            this._dictionary[domain] = {};
        this._dictionary[domain][locale] = messages;
    }
}



/***/ }),

/***/ "../packages/translation/lib/index.js":
/*!********************************************!*\
  !*** ../packages/translation/lib/index.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "nullTranslator": () => (/* reexport safe */ _base__WEBPACK_IMPORTED_MODULE_0__.nullTranslator),
/* harmony export */   "Gettext": () => (/* reexport safe */ _gettext__WEBPACK_IMPORTED_MODULE_1__.Gettext),
/* harmony export */   "TranslationManager": () => (/* reexport safe */ _manager__WEBPACK_IMPORTED_MODULE_2__.TranslationManager),
/* harmony export */   "requestTranslationsAPI": () => (/* reexport safe */ _server__WEBPACK_IMPORTED_MODULE_3__.requestTranslationsAPI),
/* harmony export */   "ITranslator": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_4__.ITranslator),
/* harmony export */   "ITranslatorConnector": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_4__.ITranslatorConnector),
/* harmony export */   "TranslatorConnector": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_4__.TranslatorConnector)
/* harmony export */ });
/* harmony import */ var _base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base */ "../packages/translation/lib/base.js");
/* harmony import */ var _gettext__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./gettext */ "../packages/translation/lib/gettext.js");
/* harmony import */ var _manager__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./manager */ "../packages/translation/lib/manager.js");
/* harmony import */ var _server__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./server */ "../packages/translation/lib/server.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./tokens */ "../packages/translation/lib/tokens.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module translation
 */
// Note: keep in alphabetical order...







/***/ }),

/***/ "../packages/translation/lib/manager.js":
/*!**********************************************!*\
  !*** ../packages/translation/lib/manager.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "TranslationManager": () => (/* binding */ TranslationManager)
/* harmony export */ });
/* harmony import */ var _gettext__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./gettext */ "../packages/translation/lib/gettext.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./tokens */ "../packages/translation/lib/tokens.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./utils */ "../packages/translation/lib/utils.js");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.



/**
 * Translation Manager
 */
class TranslationManager {
    constructor(translationsUrl = '', stringsPrefix, serverSettings) {
        this._domainData = {};
        this._translationBundles = {};
        this._connector = new _tokens__WEBPACK_IMPORTED_MODULE_1__.TranslatorConnector(translationsUrl, serverSettings);
        this._stringsPrefix = stringsPrefix || '';
        this._englishBundle = new _gettext__WEBPACK_IMPORTED_MODULE_0__.Gettext({ stringsPrefix: this._stringsPrefix });
    }
    /**
     * Fetch the localization data from the server.
     *
     * @param locale The language locale to use for translations.
     */
    async fetch(locale) {
        var _a, _b;
        this._currentLocale = locale;
        this._languageData = await this._connector.fetch({ language: locale });
        this._domainData = ((_a = this._languageData) === null || _a === void 0 ? void 0 : _a.data) || {};
        const message = (_b = this._languageData) === null || _b === void 0 ? void 0 : _b.message;
        if (message && locale !== 'en') {
            console.warn(message);
        }
    }
    /**
     * Load translation bundles for a given domain.
     *
     * @param domain The translation domain to use for translations.
     */
    load(domain) {
        if (this._domainData) {
            if (this._currentLocale == 'en') {
                return this._englishBundle;
            }
            else {
                domain = (0,_utils__WEBPACK_IMPORTED_MODULE_2__.normalizeDomain)(domain);
                if (!(domain in this._translationBundles)) {
                    let translationBundle = new _gettext__WEBPACK_IMPORTED_MODULE_0__.Gettext({
                        domain: domain,
                        locale: this._currentLocale,
                        stringsPrefix: this._stringsPrefix
                    });
                    if (domain in this._domainData) {
                        let metadata = this._domainData[domain][''];
                        if ('plural_forms' in metadata) {
                            metadata.pluralForms = metadata.plural_forms;
                            delete metadata.plural_forms;
                            this._domainData[domain][''] = metadata;
                        }
                        translationBundle.loadJSON(this._domainData[domain], domain);
                    }
                    this._translationBundles[domain] = translationBundle;
                }
                return this._translationBundles[domain];
            }
        }
        else {
            return this._englishBundle;
        }
    }
}


/***/ }),

/***/ "../packages/translation/lib/server.js":
/*!*********************************************!*\
  !*** ../packages/translation/lib/server.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestTranslationsAPI": () => (/* binding */ requestTranslationsAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * The url for the translations service.
 */
const TRANSLATIONS_SETTINGS_URL = 'api/translations';
/**
 * Call the API extension
 *
 * @param locale API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestTranslationsAPI(translationsUrl = '', locale = '', init = {}, serverSettings = undefined) {
    // Make request to Jupyter API
    const settings = serverSettings !== null && serverSettings !== void 0 ? serverSettings : _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    translationsUrl =
        translationsUrl || `${settings.appUrl}/${TRANSLATIONS_SETTINGS_URL}/`;
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, translationsUrl, locale);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.error('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "../packages/translation/lib/tokens.js":
/*!*********************************************!*\
  !*** ../packages/translation/lib/tokens.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ITranslatorConnector": () => (/* binding */ ITranslatorConnector),
/* harmony export */   "TranslatorConnector": () => (/* binding */ TranslatorConnector),
/* harmony export */   "ITranslator": () => (/* binding */ ITranslator)
/* harmony export */ });
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _server__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./server */ "../packages/translation/lib/server.js");
/* ----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/



const ITranslatorConnector = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.Token('@jupyterlab/translation:ITranslatorConnector');
class TranslatorConnector extends _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__.DataConnector {
    constructor(translationsUrl = '', serverSettings) {
        super();
        this._translationsUrl = translationsUrl;
        this._serverSettings = serverSettings;
    }
    async fetch(opts) {
        return (0,_server__WEBPACK_IMPORTED_MODULE_2__.requestTranslationsAPI)(this._translationsUrl, opts.language, {}, this._serverSettings);
    }
}
const ITranslator = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.Token('@jupyterlab/translation:ITranslator');


/***/ }),

/***/ "../packages/translation/lib/utils.js":
/*!********************************************!*\
  !*** ../packages/translation/lib/utils.js ***!
  \********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "normalizeDomain": () => (/* binding */ normalizeDomain)
/* harmony export */ });
/**
 * Normalize domain
 *
 * @param domain Domain to normalize
 * @returns Normalized domain
 */
function normalizeDomain(domain) {
    return domain.replace('-', '_');
}


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvdHJhbnNsYXRpb24vc3JjL2Jhc2UudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3RyYW5zbGF0aW9uL3NyYy9nZXR0ZXh0LnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy90cmFuc2xhdGlvbi9zcmMvaW5kZXgudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3RyYW5zbGF0aW9uL3NyYy9tYW5hZ2VyLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy90cmFuc2xhdGlvbi9zcmMvc2VydmVyLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy90cmFuc2xhdGlvbi9zcmMvdG9rZW5zLnRzIiwid2VicGFjazovL0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uLXRvcC8uLi9wYWNrYWdlcy90cmFuc2xhdGlvbi9zcmMvdXRpbHMudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7QUFBQSwwQ0FBMEM7QUFDMUMsMkRBQTJEO0FBRXZCO0FBR3BDOzs7R0FHRztBQUNILE1BQU0sY0FBYztJQUNsQixZQUFZLE1BQXlCO1FBQ25DLElBQUksQ0FBQyxlQUFlLEdBQUcsTUFBTSxDQUFDO0lBQ2hDLENBQUM7SUFFRCxJQUFJLENBQUMsTUFBYztRQUNqQixPQUFPLElBQUksQ0FBQyxlQUFlLENBQUM7SUFDOUIsQ0FBQztJQUVELE1BQU07UUFDSixPQUFPLElBQUksQ0FBQztJQUNkLENBQUM7Q0FHRjtBQUVEOztHQUVHO0FBQ0gsTUFBTSxrQkFBa0I7SUFDdEIsRUFBRSxDQUFDLEtBQWEsRUFBRSxHQUFHLElBQVc7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Q0FBQzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNwREQ7OzsrRUFHK0U7QUFHWDtBQUMxQjtBQUNRO0FBVTNDLE1BQU0sb0JBQW9CLEdBQUcsSUFBSSxvREFBSyxDQUMzQyw4Q0FBOEMsQ0FDL0MsQ0FBQztBQUVLLE1BQU0sbUJBQ1gsU0FBUSw4REFBdUQ7SUFFL0QsWUFDRSxrQkFBMEIsRUFBRSxFQUM1QixjQUEyQztRQUUzQyxLQUFLLEVBQUUsQ0FBQztRQUNSLElBQUksQ0FBQyxnQkFBZ0IsR0FBRyxlQUFlLENBQUM7UUFDeEMsSUFBSSxDQUFDLGVBQWUsR0FBRyxjQUFjLENBQUM7SUFDeEMsQ0FBQztJQUVELEtBQUssQ0FBQyxLQUFLLENBQUMsSUFBMEI7UUFDcEMsT0FBTywrREFBc0IsQ0FDM0IsSUFBSSxDQUFDLGdCQUFnQixFQUNyQixJQUFJLENBQUMsUUFBUSxFQUNiLEVBQUUsRUFDRixJQUFJLENBQUMsZUFBZSxDQUNyQixDQUFDO0lBQ0osQ0FBQztDQUlGO0FBaUZNLE1BQU0sV0FBVyxHQUFHLElBQUksb0RBQUssQ0FDbEMscUNBQXFDLENBQ3RDLENBQUM7Ozs7Ozs7Ozs7Ozs7Ozs7QUNoSUY7Ozs7O0dBS0c7QUFDSSxTQUFTLGVBQWUsQ0FBQyxNQUFjO0lBQzVDLE9BQU8sTUFBTSxDQUFDLE9BQU8sQ0FBQyxHQUFHLEVBQUUsR0FBRyxDQUFDLENBQUM7QUFDbEMsQ0FBQyIsImZpbGUiOiJwYWNrYWdlc190cmFuc2xhdGlvbl9saWJfaW5kZXhfanMuNTFhY2NjNzMwODBjMzU4ZDIwMDguanMiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IEdldHRleHQgfSBmcm9tICcuL2dldHRleHQnO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IsIFRyYW5zbGF0aW9uQnVuZGxlIH0gZnJvbSAnLi90b2tlbnMnO1xuXG4vKipcbiAqIEEgdHJhbnNsYXRvciB0aGF0IGxvYWRzIGEgZHVtbXkgbGFuZ3VhZ2UgYnVuZGxlIHRoYXQgcmV0dXJucyB0aGUgc2FtZSBpbnB1dFxuICogc3RyaW5ncy5cbiAqL1xuY2xhc3MgTnVsbFRyYW5zbGF0b3IgaW1wbGVtZW50cyBJVHJhbnNsYXRvciB7XG4gIGNvbnN0cnVjdG9yKGJ1bmRsZTogVHJhbnNsYXRpb25CdW5kbGUpIHtcbiAgICB0aGlzLl9sYW5ndWFnZUJ1bmRsZSA9IGJ1bmRsZTtcbiAgfVxuXG4gIGxvYWQoZG9tYWluOiBzdHJpbmcpOiBUcmFuc2xhdGlvbkJ1bmRsZSB7XG4gICAgcmV0dXJuIHRoaXMuX2xhbmd1YWdlQnVuZGxlO1xuICB9XG5cbiAgbG9jYWxlKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuICdlbic7XG4gIH1cblxuICBwcml2YXRlIF9sYW5ndWFnZUJ1bmRsZTogVHJhbnNsYXRpb25CdW5kbGU7XG59XG5cbi8qKlxuICogQSBsYW5ndWFnZSBidW5kbGUgdGhhdCByZXR1cm5zIHRoZSBzYW1lIGlucHV0IHN0cmluZ3MuXG4gKi9cbmNsYXNzIE51bGxMYW5ndWFnZUJ1bmRsZSB7XG4gIF9fKG1zZ2lkOiBzdHJpbmcsIC4uLmFyZ3M6IGFueVtdKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5nZXR0ZXh0KG1zZ2lkLCAuLi5hcmdzKTtcbiAgfVxuXG4gIF9uKG1zZ2lkOiBzdHJpbmcsIG1zZ2lkX3BsdXJhbDogc3RyaW5nLCBuOiBudW1iZXIsIC4uLmFyZ3M6IGFueVtdKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5uZ2V0dGV4dChtc2dpZCwgbXNnaWRfcGx1cmFsLCBuLCAuLi5hcmdzKTtcbiAgfVxuXG4gIF9wKG1zZ2N0eHQ6IHN0cmluZywgbXNnaWQ6IHN0cmluZywgLi4uYXJnczogYW55W10pOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLnBnZXR0ZXh0KG1zZ2N0eHQsIG1zZ2lkLCAuLi5hcmdzKTtcbiAgfVxuXG4gIF9ucChcbiAgICBtc2djdHh0OiBzdHJpbmcsXG4gICAgbXNnaWQ6IHN0cmluZyxcbiAgICBtc2dpZF9wbHVyYWw6IHN0cmluZyxcbiAgICBuOiBudW1iZXIsXG4gICAgLi4uYXJnczogYW55W11cbiAgKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5ucGdldHRleHQobXNnY3R4dCwgbXNnaWQsIG1zZ2lkX3BsdXJhbCwgbiwgLi4uYXJncyk7XG4gIH1cblxuICBnZXR0ZXh0KG1zZ2lkOiBzdHJpbmcsIC4uLmFyZ3M6IGFueVtdKTogc3RyaW5nIHtcbiAgICByZXR1cm4gR2V0dGV4dC5zdHJmbXQobXNnaWQsIC4uLmFyZ3MpO1xuICB9XG5cbiAgbmdldHRleHQoXG4gICAgbXNnaWQ6IHN0cmluZyxcbiAgICBtc2dpZF9wbHVyYWw6IHN0cmluZyxcbiAgICBuOiBudW1iZXIsXG4gICAgLi4uYXJnczogYW55W11cbiAgKTogc3RyaW5nIHtcbiAgICByZXR1cm4gR2V0dGV4dC5zdHJmbXQobiA9PSAxID8gbXNnaWQgOiBtc2dpZF9wbHVyYWwsIC4uLltuXS5jb25jYXQoYXJncykpO1xuICB9XG5cbiAgcGdldHRleHQobXNnY3R4dDogc3RyaW5nLCBtc2dpZDogc3RyaW5nLCAuLi5hcmdzOiBhbnlbXSk6IHN0cmluZyB7XG4gICAgcmV0dXJuIEdldHRleHQuc3RyZm10KG1zZ2lkLCAuLi5hcmdzKTtcbiAgfVxuXG4gIG5wZ2V0dGV4dChcbiAgICBtc2djdHh0OiBzdHJpbmcsXG4gICAgbXNnaWQ6IHN0cmluZyxcbiAgICBtc2dpZF9wbHVyYWw6IHN0cmluZyxcbiAgICBuOiBudW1iZXIsXG4gICAgLi4uYXJnczogYW55W11cbiAgKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5uZ2V0dGV4dChtc2dpZCwgbXNnaWRfcGx1cmFsLCBuLCAuLi5hcmdzKTtcbiAgfVxuXG4gIGRjbnBnZXR0ZXh0KFxuICAgIGRvbWFpbjogc3RyaW5nLFxuICAgIG1zZ2N0eHQ6IHN0cmluZyxcbiAgICBtc2dpZDogc3RyaW5nLFxuICAgIG1zZ2lkX3BsdXJhbDogc3RyaW5nLFxuICAgIG46IG51bWJlcixcbiAgICAuLi5hcmdzOiBhbnlbXVxuICApOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLm5nZXR0ZXh0KG1zZ2lkLCBtc2dpZF9wbHVyYWwsIG4sIC4uLmFyZ3MpO1xuICB9XG59XG5cbi8qKlxuICogVGhlIGFwcGxpY2F0aW9uIG51bGwgdHJhbnNsYXRvciBpbnN0YW5jZSB0aGF0IGp1c3QgcmV0dXJucyB0aGUgc2FtZSB0ZXh0LlxuICogQWxzbyBwcm92aWRlcyBpbnRlcnBvbGF0aW9uLlxuICovXG5leHBvcnQgY29uc3QgbnVsbFRyYW5zbGF0b3IgPSBuZXcgTnVsbFRyYW5zbGF0b3IobmV3IE51bGxMYW5ndWFnZUJ1bmRsZSgpKTtcbiIsIi8qIC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cbnwgQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG58IERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG58XG58IEJhc2UgZ2V0dGV4dC5qcyBpbXBsZW1lbnRhdGlvbi5cbnwgQ29weXJpZ2h0IChjKSBHdWlsbGF1bWUgUG90aWVyLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIE1JVCBMaWNlbnNlLlxufCBTZWU6IGh0dHBzOi8vZ2l0aHViLmNvbS9ndWlsbGF1bWVwb3RpZXIvZ2V0dGV4dC5qc1xufFxufCBUeXBlIGRlZmluaXRpb25zLlxufCBDb3B5cmlnaHQgKGMpIEp1bGllbiBDcm91emV0IGFuZCBGbG9yaWFuIFNjaHdpbmdlbnNjaGzDtmdsLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIE1JVCBMaWNlbnNlLlxufCBTZWU6IGh0dHBzOi8vZ2l0aHViLmNvbS9EZWZpbml0ZWx5VHlwZWQvRGVmaW5pdGVseVR5cGVkXG58LS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLSovXG5cbmltcG9ydCB7IG5vcm1hbGl6ZURvbWFpbiB9IGZyb20gJy4vdXRpbHMnO1xuXG4vKipcbiAqIEEgcGx1cmFsIGZvcm0gZnVuY3Rpb24uXG4gKi9cbnR5cGUgUGx1cmFsRm9ybSA9IChuOiBudW1iZXIpID0+IG51bWJlcjtcblxuLyoqXG4gKiBNZXRhZGF0YSBmb3IgYSBsYW5ndWFnZSBwYWNrLlxuICovXG5pbnRlcmZhY2UgSUpzb25EYXRhSGVhZGVyIHtcbiAgLyoqXG4gICAqIExhbmd1YWdlIGxvY2FsZS4gRXhhbXBsZTogZXNfQ08sIGVzLUNPLlxuICAgKi9cbiAgbGFuZ3VhZ2U6IHN0cmluZztcblxuICAvKipcbiAgICogVGhlIGRvbWFpbiBvZiB0aGUgdHJhbnNsYXRpb24sIHVzdWFsbHkgdGhlIG5vcm1hbGl6ZWQgcGFja2FnZSBuYW1lLlxuICAgKiBFeGFtcGxlOiBcImp1cHl0ZXJsYWJcIiwgXCJqdXB5dGVybGFiX2dpdFwiXG4gICAqXG4gICAqICMjIyMgTm90ZVxuICAgKiBOb3JtYWxpemF0aW9uIHJlcGxhY2VzIGAtYCBieSBgX2AgaW4gcGFja2FnZSBuYW1lLlxuICAgKi9cbiAgZG9tYWluOiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIFN0cmluZyBkZXNjcmliaW5nIHRoZSBwbHVyYWwgb2YgdGhlIGdpdmVuIGxhbmd1YWdlLlxuICAgKiBTZWU6IGh0dHBzOi8vd3d3LmdudS5vcmcvc29mdHdhcmUvZ2V0dGV4dC9tYW51YWwvaHRtbF9ub2RlL1RyYW5zbGF0aW5nLXBsdXJhbC1mb3Jtcy5odG1sXG4gICAqL1xuICBwbHVyYWxGb3Jtczogc3RyaW5nO1xufVxuXG4vKipcbiAqIFRyYW5zbGF0YWJsZSBzdHJpbmcgbWVzc2FnZXMuXG4gKi9cbmludGVyZmFjZSBJSnNvbkRhdGFNZXNzYWdlcyB7XG4gIC8qKlxuICAgKiBUcmFuc2xhdGlvbiBzdHJpbmdzIGZvciBhIGdpdmVuIG1zZ19pZC5cbiAgICovXG4gIFtrZXk6IHN0cmluZ106IHN0cmluZ1tdIHwgSUpzb25EYXRhSGVhZGVyO1xufVxuXG4vKipcbiAqIFRyYW5zbGF0YWJsZSBzdHJpbmcgbWVzc2FnZXMgaW5jbHVpbmcgbWV0YWRhdGEuXG4gKi9cbmludGVyZmFjZSBJSnNvbkRhdGEgZXh0ZW5kcyBJSnNvbkRhdGFNZXNzYWdlcyB7XG4gIC8qKlxuICAgKiBNZXRhZGF0YSBvZiB0aGUgbGFuZ3VhZ2UgYnVuZGxlLlxuICAgKi9cbiAgJyc6IElKc29uRGF0YUhlYWRlcjtcbn1cblxuLyoqXG4gKiBDb25maWd1cmFibGUgb3B0aW9ucyBmb3IgdGhlIEdldHRleHQgY29uc3RydWN0b3IuXG4gKi9cbmludGVyZmFjZSBJT3B0aW9ucyB7XG4gIC8qKlxuICAgKiBMYW5ndWFnZSBsb2NhbGUuIEV4YW1wbGU6IGVzX0NPLCBlcy1DTy5cbiAgICovXG4gIGxvY2FsZT86IHN0cmluZztcblxuICAvKipcbiAgICogVGhlIGRvbWFpbiBvZiB0aGUgdHJhbnNsYXRpb24sIHVzdWFsbHkgdGhlIG5vcm1hbGl6ZWQgcGFja2FnZSBuYW1lLlxuICAgKiBFeGFtcGxlOiBcImp1cHl0ZXJsYWJcIiwgXCJqdXB5dGVybGFiX2dpdFwiXG4gICAqXG4gICAqICMjIyMgTm90ZVxuICAgKiBOb3JtYWxpemF0aW9uIHJlcGxhY2VzIGAtYCBieSBgX2AgaW4gcGFja2FnZSBuYW1lLlxuICAgKi9cbiAgZG9tYWluPzogc3RyaW5nO1xuXG4gIC8qKlxuICAgKiBUaGUgZGVsaW1pdGVyIHRvIHVzZSB3aGVuIGFkZGluZyBjb250ZXh0dWFsaXplZCBzdHJpbmdzLlxuICAgKi9cbiAgY29udGV4dERlbGltaXRlcj86IHN0cmluZztcblxuICAvKipcbiAgICogVHJhbnNsYXRpb24gbWVzc2FnZSBzdHJpbmdzLlxuICAgKi9cbiAgbWVzc2FnZXM/OiBBcnJheTxzdHJpbmc+O1xuXG4gIC8qKlxuICAgKiBTdHJpbmcgZGVzY3JpYmluZyB0aGUgcGx1cmFsIG9mIHRoZSBnaXZlbiBsYW5ndWFnZS5cbiAgICogU2VlOiBodHRwczovL3d3dy5nbnUub3JnL3NvZnR3YXJlL2dldHRleHQvbWFudWFsL2h0bWxfbm9kZS9UcmFuc2xhdGluZy1wbHVyYWwtZm9ybXMuaHRtbFxuICAgKi9cbiAgcGx1cmFsRm9ybXM/OiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIFRoZSBzdHJpbmcgcHJlZml4IHRvIGFkZCB0byBsb2NhbGl6ZWQgc3RyaW5ncy5cbiAgICovXG4gIHN0cmluZ3NQcmVmaXg/OiBzdHJpbmc7XG5cbiAgLyoqXG4gICAqIFBsdXJhbCBmb3JtIGZ1bmN0aW9uLlxuICAgKi9cbiAgcGx1cmFsRnVuYz86IFBsdXJhbEZvcm07XG59XG5cbi8qKlxuICogT3B0aW9ucyBvZiB0aGUgbWFpbiB0cmFuc2xhdGlvbiBgdGAgbWV0aG9kLlxuICovXG5pbnRlcmZhY2UgSVRPcHRpb25zIHtcbiAgLyoqXG4gICAqIFN0cmluZyBkZXNjcmliaW5nIHRoZSBwbHVyYWwgb2YgdGhlIGdpdmVuIGxhbmd1YWdlLlxuICAgKiBTZWU6IGh0dHBzOi8vd3d3LmdudS5vcmcvc29mdHdhcmUvZ2V0dGV4dC9tYW51YWwvaHRtbF9ub2RlL1RyYW5zbGF0aW5nLXBsdXJhbC1mb3Jtcy5odG1sXG4gICAqL1xuICBwbHVyYWxGb3JtPzogc3RyaW5nO1xuXG4gIC8qKlxuICAgKiBQbHVyYWwgZm9ybSBmdW5jdGlvbi5cbiAgICovXG4gIHBsdXJhbEZ1bmM/OiBQbHVyYWxGb3JtO1xuXG4gIC8qKlxuICAgKiBMYW5ndWFnZSBsb2NhbGUuIEV4YW1wbGU6IGVzX0NPLCBlcy1DTy5cbiAgICovXG4gIGxvY2FsZT86IHN0cmluZztcbn1cblxuLyoqXG4gKiBHZXR0ZXh0IGNsYXNzIHByb3ZpZGluZyBsb2NhbGl6YXRpb24gbWV0aG9kcy5cbiAqL1xuY2xhc3MgR2V0dGV4dCB7XG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM/OiBJT3B0aW9ucykge1xuICAgIG9wdGlvbnMgPSBvcHRpb25zIHx8IHt9O1xuXG4gICAgLy8gZGVmYXVsdCB2YWx1ZXMgdGhhdCBjb3VsZCBiZSBvdmVycmlkZGVuIGluIEdldHRleHQoKSBjb25zdHJ1Y3RvclxuICAgIHRoaXMuX2RlZmF1bHRzID0ge1xuICAgICAgZG9tYWluOiAnbWVzc2FnZXMnLFxuICAgICAgbG9jYWxlOiBkb2N1bWVudC5kb2N1bWVudEVsZW1lbnQuZ2V0QXR0cmlidXRlKCdsYW5nJykgfHwgJ2VuJyxcbiAgICAgIHBsdXJhbEZ1bmM6IGZ1bmN0aW9uIChuOiBudW1iZXIpIHtcbiAgICAgICAgcmV0dXJuIHsgbnBsdXJhbHM6IDIsIHBsdXJhbDogbiAhPSAxID8gMSA6IDAgfTtcbiAgICAgIH0sXG4gICAgICBjb250ZXh0RGVsaW1pdGVyOiBTdHJpbmcuZnJvbUNoYXJDb2RlKDQpLCAvLyBcXHUwMDA0XG4gICAgICBzdHJpbmdzUHJlZml4OiAnJ1xuICAgIH07XG5cbiAgICAvLyBFbnN1cmUgdGhlIGNvcnJlY3Qgc2VwYXJhdG9yIGlzIHVzZWRcbiAgICB0aGlzLl9sb2NhbGUgPSAob3B0aW9ucy5sb2NhbGUgfHwgdGhpcy5fZGVmYXVsdHMubG9jYWxlKS5yZXBsYWNlKCdfJywgJy0nKTtcbiAgICB0aGlzLl9kb21haW4gPSBub3JtYWxpemVEb21haW4ob3B0aW9ucy5kb21haW4gfHwgdGhpcy5fZGVmYXVsdHMuZG9tYWluKTtcbiAgICB0aGlzLl9jb250ZXh0RGVsaW1pdGVyID1cbiAgICAgIG9wdGlvbnMuY29udGV4dERlbGltaXRlciB8fCB0aGlzLl9kZWZhdWx0cy5jb250ZXh0RGVsaW1pdGVyO1xuICAgIHRoaXMuX3N0cmluZ3NQcmVmaXggPSBvcHRpb25zLnN0cmluZ3NQcmVmaXggfHwgdGhpcy5fZGVmYXVsdHMuc3RyaW5nc1ByZWZpeDtcbiAgICB0aGlzLl9wbHVyYWxGdW5jcyA9IHt9O1xuICAgIHRoaXMuX2RpY3Rpb25hcnkgPSB7fTtcbiAgICB0aGlzLl9wbHVyYWxGb3JtcyA9IHt9O1xuXG4gICAgaWYgKG9wdGlvbnMubWVzc2FnZXMpIHtcbiAgICAgIHRoaXMuX2RpY3Rpb25hcnlbdGhpcy5fZG9tYWluXSA9IHt9O1xuICAgICAgdGhpcy5fZGljdGlvbmFyeVt0aGlzLl9kb21haW5dW3RoaXMuX2xvY2FsZV0gPSBvcHRpb25zLm1lc3NhZ2VzO1xuICAgIH1cblxuICAgIGlmIChvcHRpb25zLnBsdXJhbEZvcm1zKSB7XG4gICAgICB0aGlzLl9wbHVyYWxGb3Jtc1t0aGlzLl9sb2NhbGVdID0gb3B0aW9ucy5wbHVyYWxGb3JtcztcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogU2V0IGN1cnJlbnQgY29udGV4dCBkZWxpbWl0ZXIuXG4gICAqXG4gICAqIEBwYXJhbSBkZWxpbWl0ZXIgLSBUaGUgZGVsaW1pdGVyIHRvIHNldC5cbiAgICovXG4gIHNldENvbnRleHREZWxpbWl0ZXIoZGVsaW1pdGVyOiBzdHJpbmcpOiB2b2lkIHtcbiAgICB0aGlzLl9jb250ZXh0RGVsaW1pdGVyID0gZGVsaW1pdGVyO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCBjdXJyZW50IGNvbnRleHQgZGVsaW1pdGVyLlxuICAgKlxuICAgKiBAcmV0dXJuIFRoZSBjdXJyZW50IGRlbGltaXRlci5cbiAgICovXG4gIGdldENvbnRleHREZWxpbWl0ZXIoKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5fY29udGV4dERlbGltaXRlcjtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgY3VycmVudCBsb2NhbGUuXG4gICAqXG4gICAqIEBwYXJhbSBsb2NhbGUgLSBUaGUgbG9jYWxlIHRvIHNldC5cbiAgICovXG4gIHNldExvY2FsZShsb2NhbGU6IHN0cmluZyk6IHZvaWQge1xuICAgIHRoaXMuX2xvY2FsZSA9IGxvY2FsZS5yZXBsYWNlKCdfJywgJy0nKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBHZXQgY3VycmVudCBsb2NhbGUuXG4gICAqXG4gICAqIEByZXR1cm4gVGhlIGN1cnJlbnQgbG9jYWxlLlxuICAgKi9cbiAgZ2V0TG9jYWxlKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuX2xvY2FsZTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgY3VycmVudCBkb21haW4uXG4gICAqXG4gICAqIEBwYXJhbSBkb21haW4gLSBUaGUgZG9tYWluIHRvIHNldC5cbiAgICovXG4gIHNldERvbWFpbihkb21haW46IHN0cmluZyk6IHZvaWQge1xuICAgIHRoaXMuX2RvbWFpbiA9IG5vcm1hbGl6ZURvbWFpbihkb21haW4pO1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCBjdXJyZW50IGRvbWFpbi5cbiAgICpcbiAgICogQHJldHVybiBUaGUgY3VycmVudCBkb21haW4gc3RyaW5nLlxuICAgKi9cbiAgZ2V0RG9tYWluKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuX2RvbWFpbjtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgY3VycmVudCBzdHJpbmdzIHByZWZpeC5cbiAgICpcbiAgICogQHBhcmFtIHByZWZpeCAtIFRoZSBzdHJpbmcgcHJlZml4IHRvIHNldC5cbiAgICovXG4gIHNldFN0cmluZ3NQcmVmaXgocHJlZml4OiBzdHJpbmcpOiB2b2lkIHtcbiAgICB0aGlzLl9zdHJpbmdzUHJlZml4ID0gcHJlZml4O1xuICB9XG5cbiAgLyoqXG4gICAqIEdldCBjdXJyZW50IHN0cmluZ3MgcHJlZml4LlxuICAgKlxuICAgKiBAcmV0dXJuIFRoZSBzdHJpbmdzIHByZWZpeC5cbiAgICovXG4gIGdldFN0cmluZ3NQcmVmaXgoKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5fc3RyaW5nc1ByZWZpeDtcbiAgfVxuXG4gIC8qKlxuICAgKiBgc3ByaW50ZmAgZXF1aXZhbGVudCwgdGFrZXMgYSBzdHJpbmcgYW5kIHNvbWUgYXJndW1lbnRzIHRvIG1ha2UgYVxuICAgKiBjb21wdXRlZCBzdHJpbmcuXG4gICAqXG4gICAqIEBwYXJhbSBmbXQgLSBUaGUgc3RyaW5nIHRvIGludGVycG9sYXRlLlxuICAgKiBAcGFyYW0gYXJncyAtIFRoZSB2YXJpYWJsZXMgdG8gdXNlIGluIGludGVycG9sYXRpb24uXG4gICAqXG4gICAqICMjIyBFeGFtcGxlc1xuICAgKiBzdHJmbXQoXCIlMSBkb2dzIGFyZSBpbiAlMlwiLCA3LCBcInRoZSBraXRjaGVuXCIpOyA9PiBcIjcgZG9ncyBhcmUgaW4gdGhlIGtpdGNoZW5cIlxuICAgKiBzdHJmbXQoXCJJIGxpa2UgJTEsIGJhbmFuYXMgYW5kICUxXCIsIFwiYXBwbGVzXCIpOyA9PiBcIkkgbGlrZSBhcHBsZXMsIGJhbmFuYXMgYW5kIGFwcGxlc1wiXG4gICAqL1xuICBzdGF0aWMgc3RyZm10KGZtdDogc3RyaW5nLCAuLi5hcmdzOiBhbnlbXSk6IHN0cmluZyB7XG4gICAgcmV0dXJuIChcbiAgICAgIGZtdFxuICAgICAgICAvLyBwdXQgc3BhY2UgYWZ0ZXIgZG91YmxlICUgdG8gcHJldmVudCBwbGFjZWhvbGRlciByZXBsYWNlbWVudCBvZiBzdWNoIG1hdGNoZXNcbiAgICAgICAgLnJlcGxhY2UoLyUlL2csICclJSAnKVxuICAgICAgICAvLyByZXBsYWNlIHBsYWNlaG9sZGVyc1xuICAgICAgICAucmVwbGFjZSgvJShcXGQrKS9nLCBmdW5jdGlvbiAoc3RyLCBwMSkge1xuICAgICAgICAgIHJldHVybiBhcmdzW3AxIC0gMV07XG4gICAgICAgIH0pXG4gICAgICAgIC8vIHJlcGxhY2UgZG91YmxlICUgYW5kIHNwYWNlIHdpdGggc2luZ2xlICVcbiAgICAgICAgLnJlcGxhY2UoLyUlIC9nLCAnJScpXG4gICAgKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBMb2FkIGpzb24gdHJhbnNsYXRpb25zIHN0cmluZ3MgKEluIEplZCAyLnggZm9ybWF0KS5cbiAgICpcbiAgICogQHBhcmFtIGpzb25EYXRhIC0gVGhlIHRyYW5zbGF0aW9uIHN0cmluZ3MgcGx1cyBtZXRhZGF0YS5cbiAgICogQHBhcmFtIGRvbWFpbiAtIFRoZSB0cmFuc2xhdGlvbiBkb21haW4sIGUuZy4gXCJqdXB5dGVybGFiXCIuXG4gICAqL1xuICBsb2FkSlNPTihqc29uRGF0YTogSUpzb25EYXRhLCBkb21haW46IHN0cmluZyk6IHZvaWQge1xuICAgIGlmIChcbiAgICAgICFqc29uRGF0YVsnJ10gfHxcbiAgICAgICFqc29uRGF0YVsnJ11bJ2xhbmd1YWdlJ10gfHxcbiAgICAgICFqc29uRGF0YVsnJ11bJ3BsdXJhbEZvcm1zJ11cbiAgICApIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcihcbiAgICAgICAgYFdyb25nIGpzb25EYXRhLCBpdCBtdXN0IGhhdmUgYW4gZW1wdHkga2V5IChcIlwiKSB3aXRoIFwibGFuZ3VhZ2VcIiBhbmQgXCJwbHVyYWxGb3Jtc1wiIGluZm9ybWF0aW9uOiAke2pzb25EYXRhfWBcbiAgICAgICk7XG4gICAgfVxuXG4gICAgZG9tYWluID0gbm9ybWFsaXplRG9tYWluKGRvbWFpbik7XG5cbiAgICBsZXQgaGVhZGVycyA9IGpzb25EYXRhWycnXTtcbiAgICBsZXQganNvbkRhdGFDb3B5ID0gSlNPTi5wYXJzZShKU09OLnN0cmluZ2lmeShqc29uRGF0YSkpO1xuICAgIGRlbGV0ZSBqc29uRGF0YUNvcHlbJyddO1xuXG4gICAgdGhpcy5zZXRNZXNzYWdlcyhcbiAgICAgIGRvbWFpbiB8fCB0aGlzLl9kZWZhdWx0cy5kb21haW4sXG4gICAgICBoZWFkZXJzWydsYW5ndWFnZSddLFxuICAgICAganNvbkRhdGFDb3B5LFxuICAgICAgaGVhZGVyc1sncGx1cmFsRm9ybXMnXVxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogU2hvcnRoYW5kIGZvciBnZXR0ZXh0LlxuICAgKlxuICAgKiBAcGFyYW0gbXNnaWQgLSBUaGUgc2luZ3VsYXIgc3RyaW5nIHRvIHRyYW5zbGF0ZS5cbiAgICogQHBhcmFtIGFyZ3MgLSBBbnkgYWRkaXRpb25hbCB2YWx1ZXMgdG8gdXNlIHdpdGggaW50ZXJwb2xhdGlvbi5cbiAgICpcbiAgICogQHJldHVybiBBIHRyYW5zbGF0ZWQgc3RyaW5nIGlmIGZvdW5kLCBvciB0aGUgb3JpZ2luYWwgc3RyaW5nLlxuICAgKlxuICAgKiAjIyMgTm90ZXNcbiAgICogVGhpcyBpcyBub3QgYSBwcml2YXRlIG1ldGhvZCAoc3RhcnRzIHdpdGggYW4gdW5kZXJzY29yZSkgaXQgaXMganVzdFxuICAgKiBhIHNob3J0ZXIgYW5kIHN0YW5kYXJkIHdheSB0byBjYWxsIHRoZXNlIG1ldGhvZHMuXG4gICAqL1xuICBfXyhtc2dpZDogc3RyaW5nLCAuLi5hcmdzOiBhbnlbXSk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuZ2V0dGV4dChtc2dpZCwgLi4uYXJncyk7XG4gIH1cblxuICAvKipcbiAgICogU2hvcnRoYW5kIGZvciBuZ2V0dGV4dC5cbiAgICpcbiAgICogQHBhcmFtIG1zZ2lkIC0gVGhlIHNpbmd1bGFyIHN0cmluZyB0byB0cmFuc2xhdGUuXG4gICAqIEBwYXJhbSBtc2dpZF9wbHVyYWwgLSBUaGUgcGx1cmFsIHN0cmluZyB0byB0cmFuc2xhdGUuXG4gICAqIEBwYXJhbSBuIC0gVGhlIG51bWJlciBmb3IgcGx1cmFsaXphdGlvbi5cbiAgICogQHBhcmFtIGFyZ3MgLSBBbnkgYWRkaXRpb25hbCB2YWx1ZXMgdG8gdXNlIHdpdGggaW50ZXJwb2xhdGlvbi5cbiAgICpcbiAgICogQHJldHVybiBBIHRyYW5zbGF0ZWQgc3RyaW5nIGlmIGZvdW5kLCBvciB0aGUgb3JpZ2luYWwgc3RyaW5nLlxuICAgKlxuICAgKiAjIyMgTm90ZXNcbiAgICogVGhpcyBpcyBub3QgYSBwcml2YXRlIG1ldGhvZCAoc3RhcnRzIHdpdGggYW4gdW5kZXJzY29yZSkgaXQgaXMganVzdFxuICAgKiBhIHNob3J0ZXIgYW5kIHN0YW5kYXJkIHdheSB0byBjYWxsIHRoZXNlIG1ldGhvZHMuXG4gICAqL1xuICBfbihtc2dpZDogc3RyaW5nLCBtc2dpZF9wbHVyYWw6IHN0cmluZywgbjogbnVtYmVyLCAuLi5hcmdzOiBhbnlbXSk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMubmdldHRleHQobXNnaWQsIG1zZ2lkX3BsdXJhbCwgbiwgLi4uYXJncyk7XG4gIH1cblxuICAvKipcbiAgICogU2hvcnRoYW5kIGZvciBwZ2V0dGV4dC5cbiAgICpcbiAgICogQHBhcmFtIG1zZ2N0eHQgLSBUaGUgbWVzc2FnZSBjb250ZXh0LlxuICAgKiBAcGFyYW0gbXNnaWQgLSBUaGUgc2luZ3VsYXIgc3RyaW5nIHRvIHRyYW5zbGF0ZS5cbiAgICogQHBhcmFtIGFyZ3MgLSBBbnkgYWRkaXRpb25hbCB2YWx1ZXMgdG8gdXNlIHdpdGggaW50ZXJwb2xhdGlvbi5cbiAgICpcbiAgICogQHJldHVybiBBIHRyYW5zbGF0ZWQgc3RyaW5nIGlmIGZvdW5kLCBvciB0aGUgb3JpZ2luYWwgc3RyaW5nLlxuICAgKlxuICAgKiAjIyMgTm90ZXNcbiAgICogVGhpcyBpcyBub3QgYSBwcml2YXRlIG1ldGhvZCAoc3RhcnRzIHdpdGggYW4gdW5kZXJzY29yZSkgaXQgaXMganVzdFxuICAgKiBhIHNob3J0ZXIgYW5kIHN0YW5kYXJkIHdheSB0byBjYWxsIHRoZXNlIG1ldGhvZHMuXG4gICAqL1xuICBfcChtc2djdHh0OiBzdHJpbmcsIG1zZ2lkOiBzdHJpbmcsIC4uLmFyZ3M6IGFueVtdKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5wZ2V0dGV4dChtc2djdHh0LCBtc2dpZCwgLi4uYXJncyk7XG4gIH1cblxuICAvKipcbiAgICogU2hvcnRoYW5kIGZvciBucGdldHRleHQuXG4gICAqXG4gICAqIEBwYXJhbSBtc2djdHh0IC0gVGhlIG1lc3NhZ2UgY29udGV4dC5cbiAgICogQHBhcmFtIG1zZ2lkIC0gVGhlIHNpbmd1bGFyIHN0cmluZyB0byB0cmFuc2xhdGUuXG4gICAqIEBwYXJhbSBtc2dpZF9wbHVyYWwgLSBUaGUgcGx1cmFsIHN0cmluZyB0byB0cmFuc2xhdGUuXG4gICAqIEBwYXJhbSBuIC0gVGhlIG51bWJlciBmb3IgcGx1cmFsaXphdGlvbi5cbiAgICogQHBhcmFtIGFyZ3MgLSBBbnkgYWRkaXRpb25hbCB2YWx1ZXMgdG8gdXNlIHdpdGggaW50ZXJwb2xhdGlvbi5cbiAgICpcbiAgICogQHJldHVybiBBIHRyYW5zbGF0ZWQgc3RyaW5nIGlmIGZvdW5kLCBvciB0aGUgb3JpZ2luYWwgc3RyaW5nLlxuICAgKlxuICAgKiAjIyMgTm90ZXNcbiAgICogVGhpcyBpcyBub3QgYSBwcml2YXRlIG1ldGhvZCAoc3RhcnRzIHdpdGggYW4gdW5kZXJzY29yZSkgaXQgaXMganVzdFxuICAgKiBhIHNob3J0ZXIgYW5kIHN0YW5kYXJkIHdheSB0byBjYWxsIHRoZXNlIG1ldGhvZHMuXG4gICAqL1xuICBfbnAoXG4gICAgbXNnY3R4dDogc3RyaW5nLFxuICAgIG1zZ2lkOiBzdHJpbmcsXG4gICAgbXNnaWRfcGx1cmFsOiBzdHJpbmcsXG4gICAgbjogbnVtYmVyLFxuICAgIC4uLmFyZ3M6IGFueVtdXG4gICk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMubnBnZXR0ZXh0KG1zZ2N0eHQsIG1zZ2lkLCBtc2dpZF9wbHVyYWwsIG4sIC4uLmFyZ3MpO1xuICB9XG5cbiAgLyoqXG4gICAqIFRyYW5zbGF0ZSBhIHNpbmd1bGFyIHN0cmluZyB3aXRoIGV4dHJhIGludGVycG9sYXRpb24gdmFsdWVzLlxuICAgKlxuICAgKiBAcGFyYW0gbXNnaWQgLSBUaGUgc2luZ3VsYXIgc3RyaW5nIHRvIHRyYW5zbGF0ZS5cbiAgICogQHBhcmFtIGFyZ3MgLSBBbnkgYWRkaXRpb25hbCB2YWx1ZXMgdG8gdXNlIHdpdGggaW50ZXJwb2xhdGlvbi5cbiAgICpcbiAgICogQHJldHVybiBBIHRyYW5zbGF0ZWQgc3RyaW5nIGlmIGZvdW5kLCBvciB0aGUgb3JpZ2luYWwgc3RyaW5nLlxuICAgKi9cbiAgZ2V0dGV4dChtc2dpZDogc3RyaW5nLCAuLi5hcmdzOiBhbnlbXSk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuZGNucGdldHRleHQoJycsICcnLCBtc2dpZCwgJycsIDAsIC4uLmFyZ3MpO1xuICB9XG5cbiAgLyoqXG4gICAqIFRyYW5zbGF0ZSBhIHBsdXJhbCBzdHJpbmcgd2l0aCBleHRyYSBpbnRlcnBvbGF0aW9uIHZhbHVlcy5cbiAgICpcbiAgICogQHBhcmFtIG1zZ2lkIC0gVGhlIHNpbmd1bGFyIHN0cmluZyB0byB0cmFuc2xhdGUuXG4gICAqIEBwYXJhbSBhcmdzIC0gQW55IGFkZGl0aW9uYWwgdmFsdWVzIHRvIHVzZSB3aXRoIGludGVycG9sYXRpb24uXG4gICAqXG4gICAqIEByZXR1cm4gQSB0cmFuc2xhdGVkIHN0cmluZyBpZiBmb3VuZCwgb3IgdGhlIG9yaWdpbmFsIHN0cmluZy5cbiAgICovXG4gIG5nZXR0ZXh0KFxuICAgIG1zZ2lkOiBzdHJpbmcsXG4gICAgbXNnaWRfcGx1cmFsOiBzdHJpbmcsXG4gICAgbjogbnVtYmVyLFxuICAgIC4uLmFyZ3M6IGFueVtdXG4gICk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuZGNucGdldHRleHQoJycsICcnLCBtc2dpZCwgbXNnaWRfcGx1cmFsLCBuLCAuLi5hcmdzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUcmFuc2xhdGUgYSBjb250ZXh0dWFsaXplZCBzaW5ndWxhciBzdHJpbmcgd2l0aCBleHRyYSBpbnRlcnBvbGF0aW9uIHZhbHVlcy5cbiAgICpcbiAgICogQHBhcmFtIG1zZ2N0eHQgLSBUaGUgbWVzc2FnZSBjb250ZXh0LlxuICAgKiBAcGFyYW0gbXNnaWQgLSBUaGUgc2luZ3VsYXIgc3RyaW5nIHRvIHRyYW5zbGF0ZS5cbiAgICogQHBhcmFtIGFyZ3MgLSBBbnkgYWRkaXRpb25hbCB2YWx1ZXMgdG8gdXNlIHdpdGggaW50ZXJwb2xhdGlvbi5cbiAgICpcbiAgICogQHJldHVybiBBIHRyYW5zbGF0ZWQgc3RyaW5nIGlmIGZvdW5kLCBvciB0aGUgb3JpZ2luYWwgc3RyaW5nLlxuICAgKlxuICAgKiAjIyMgTm90ZXNcbiAgICogVGhpcyBpcyBub3QgYSBwcml2YXRlIG1ldGhvZCAoc3RhcnRzIHdpdGggYW4gdW5kZXJzY29yZSkgaXQgaXMganVzdFxuICAgKiBhIHNob3J0ZXIgYW5kIHN0YW5kYXJkIHdheSB0byBjYWxsIHRoZXNlIG1ldGhvZHMuXG4gICAqL1xuICBwZ2V0dGV4dChtc2djdHh0OiBzdHJpbmcsIG1zZ2lkOiBzdHJpbmcsIC4uLmFyZ3M6IGFueVtdKTogc3RyaW5nIHtcbiAgICByZXR1cm4gdGhpcy5kY25wZ2V0dGV4dCgnJywgbXNnY3R4dCwgbXNnaWQsICcnLCAwLCAuLi5hcmdzKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUcmFuc2xhdGUgYSBjb250ZXh0dWFsaXplZCBwbHVyYWwgc3RyaW5nIHdpdGggZXh0cmEgaW50ZXJwb2xhdGlvbiB2YWx1ZXMuXG4gICAqXG4gICAqIEBwYXJhbSBtc2djdHh0IC0gVGhlIG1lc3NhZ2UgY29udGV4dC5cbiAgICogQHBhcmFtIG1zZ2lkIC0gVGhlIHNpbmd1bGFyIHN0cmluZyB0byB0cmFuc2xhdGUuXG4gICAqIEBwYXJhbSBtc2dpZF9wbHVyYWwgLSBUaGUgcGx1cmFsIHN0cmluZyB0byB0cmFuc2xhdGUuXG4gICAqIEBwYXJhbSBuIC0gVGhlIG51bWJlciBmb3IgcGx1cmFsaXphdGlvbi5cbiAgICogQHBhcmFtIGFyZ3MgLSBBbnkgYWRkaXRpb25hbCB2YWx1ZXMgdG8gdXNlIHdpdGggaW50ZXJwb2xhdGlvblxuICAgKlxuICAgKiBAcmV0dXJuIEEgdHJhbnNsYXRlZCBzdHJpbmcgaWYgZm91bmQsIG9yIHRoZSBvcmlnaW5hbCBzdHJpbmcuXG4gICAqL1xuICBucGdldHRleHQoXG4gICAgbXNnY3R4dDogc3RyaW5nLFxuICAgIG1zZ2lkOiBzdHJpbmcsXG4gICAgbXNnaWRfcGx1cmFsOiBzdHJpbmcsXG4gICAgbjogbnVtYmVyLFxuICAgIC4uLmFyZ3M6IGFueVtdXG4gICk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMuZGNucGdldHRleHQoJycsIG1zZ2N0eHQsIG1zZ2lkLCBtc2dpZF9wbHVyYWwsIG4sIC4uLmFyZ3MpO1xuICB9XG5cbiAgLyoqXG4gICAqIFRyYW5zbGF0ZSBhIHNpbmd1bGFyIHN0cmluZyB3aXRoIGV4dHJhIGludGVycG9sYXRpb24gdmFsdWVzLlxuICAgKlxuICAgKiBAcGFyYW0gZG9tYWluIC0gVGhlIHRyYW5zbGF0aW9ucyBkb21haW4uXG4gICAqIEBwYXJhbSBtc2djdHh0IC0gVGhlIG1lc3NhZ2UgY29udGV4dC5cbiAgICogQHBhcmFtIG1zZ2lkIC0gVGhlIHNpbmd1bGFyIHN0cmluZyB0byB0cmFuc2xhdGUuXG4gICAqIEBwYXJhbSBtc2dpZF9wbHVyYWwgLSBUaGUgcGx1cmFsIHN0cmluZyB0byB0cmFuc2xhdGUuXG4gICAqIEBwYXJhbSBuIC0gVGhlIG51bWJlciBmb3IgcGx1cmFsaXphdGlvbi5cbiAgICogQHBhcmFtIGFyZ3MgLSBBbnkgYWRkaXRpb25hbCB2YWx1ZXMgdG8gdXNlIHdpdGggaW50ZXJwb2xhdGlvblxuICAgKlxuICAgKiBAcmV0dXJuIEEgdHJhbnNsYXRlZCBzdHJpbmcgaWYgZm91bmQsIG9yIHRoZSBvcmlnaW5hbCBzdHJpbmcuXG4gICAqL1xuICBkY25wZ2V0dGV4dChcbiAgICBkb21haW46IHN0cmluZyxcbiAgICBtc2djdHh0OiBzdHJpbmcsXG4gICAgbXNnaWQ6IHN0cmluZyxcbiAgICBtc2dpZF9wbHVyYWw6IHN0cmluZyxcbiAgICBuOiBudW1iZXIsXG4gICAgLi4uYXJnczogYW55W11cbiAgKTogc3RyaW5nIHtcbiAgICBkb21haW4gPSBub3JtYWxpemVEb21haW4oZG9tYWluKSB8fCB0aGlzLl9kb21haW47XG5cbiAgICBsZXQgdHJhbnNsYXRpb246IEFycmF5PHN0cmluZz47XG4gICAgbGV0IGtleTogc3RyaW5nID0gbXNnY3R4dFxuICAgICAgPyBtc2djdHh0ICsgdGhpcy5fY29udGV4dERlbGltaXRlciArIG1zZ2lkXG4gICAgICA6IG1zZ2lkO1xuICAgIGxldCBvcHRpb25zOiBhbnkgPSB7IHBsdXJhbEZvcm06IGZhbHNlIH07XG4gICAgbGV0IGV4aXN0OiBib29sZWFuID0gZmFsc2U7XG4gICAgbGV0IGxvY2FsZTogc3RyaW5nID0gdGhpcy5fbG9jYWxlO1xuICAgIGxldCBsb2NhbGVzID0gdGhpcy5leHBhbmRMb2NhbGUodGhpcy5fbG9jYWxlKTtcblxuICAgIGZvciAobGV0IGkgaW4gbG9jYWxlcykge1xuICAgICAgbG9jYWxlID0gbG9jYWxlc1tpXTtcbiAgICAgIGV4aXN0ID1cbiAgICAgICAgdGhpcy5fZGljdGlvbmFyeVtkb21haW5dICYmXG4gICAgICAgIHRoaXMuX2RpY3Rpb25hcnlbZG9tYWluXVtsb2NhbGVdICYmXG4gICAgICAgIHRoaXMuX2RpY3Rpb25hcnlbZG9tYWluXVtsb2NhbGVdW2tleV07XG5cbiAgICAgIC8vIGNoZWNrIGNvbmRpdGlvbiBhcmUgdmFsaWQgKC5sZW5ndGgpXG4gICAgICAvLyBiZWNhdXNlIGl0J3Mgbm90IHBvc3NpYmxlIHRvIGRlZmluZSBib3RoIGEgc2luZ3VsYXIgYW5kIGEgcGx1cmFsIGZvcm0gb2YgdGhlIHNhbWUgbXNnaWQsXG4gICAgICAvLyB3ZSBuZWVkIHRvIGNoZWNrIHRoYXQgdGhlIHN0b3JlZCBmb3JtIGlzIHRoZSBzYW1lIGFzIHRoZSBleHBlY3RlZCBvbmUuXG4gICAgICAvLyBpZiBub3QsIHdlJ2xsIGp1c3QgaWdub3JlIHRoZSB0cmFuc2xhdGlvbiBhbmQgY29uc2lkZXIgaXQgYXMgbm90IHRyYW5zbGF0ZWQuXG4gICAgICBpZiAobXNnaWRfcGx1cmFsKSB7XG4gICAgICAgIGV4aXN0ID0gZXhpc3QgJiYgdGhpcy5fZGljdGlvbmFyeVtkb21haW5dW2xvY2FsZV1ba2V5XS5sZW5ndGggPiAxO1xuICAgICAgfSBlbHNlIHtcbiAgICAgICAgZXhpc3QgPSBleGlzdCAmJiB0aGlzLl9kaWN0aW9uYXJ5W2RvbWFpbl1bbG9jYWxlXVtrZXldLmxlbmd0aCA9PSAxO1xuICAgICAgfVxuXG4gICAgICBpZiAoZXhpc3QpIHtcbiAgICAgICAgLy8gVGhpcyBlbnN1cmVzIHRoYXQgYSB2YXJpYXRpb24gaXMgdXNlZC5cbiAgICAgICAgb3B0aW9ucy5sb2NhbGUgPSBsb2NhbGU7XG4gICAgICAgIGJyZWFrO1xuICAgICAgfVxuICAgIH1cblxuICAgIGlmICghZXhpc3QpIHtcbiAgICAgIHRyYW5zbGF0aW9uID0gW21zZ2lkXTtcbiAgICAgIG9wdGlvbnMucGx1cmFsRnVuYyA9IHRoaXMuX2RlZmF1bHRzLnBsdXJhbEZ1bmM7XG4gICAgfSBlbHNlIHtcbiAgICAgIHRyYW5zbGF0aW9uID0gdGhpcy5fZGljdGlvbmFyeVtkb21haW5dW2xvY2FsZV1ba2V5XTtcbiAgICB9XG5cbiAgICAvLyBTaW5ndWxhciBmb3JtXG4gICAgaWYgKCFtc2dpZF9wbHVyYWwpIHtcbiAgICAgIHJldHVybiB0aGlzLnQodHJhbnNsYXRpb24sIG4sIG9wdGlvbnMsIC4uLmFyZ3MpO1xuICAgIH1cblxuICAgIC8vIFBsdXJhbCBvbmVcbiAgICBvcHRpb25zLnBsdXJhbEZvcm0gPSB0cnVlO1xuICAgIGxldCB2YWx1ZTogQXJyYXk8c3RyaW5nPiA9IGV4aXN0ID8gdHJhbnNsYXRpb24gOiBbbXNnaWQsIG1zZ2lkX3BsdXJhbF07XG4gICAgcmV0dXJuIHRoaXMudCh2YWx1ZSwgbiwgb3B0aW9ucywgLi4uYXJncyk7XG4gIH1cblxuICAvKipcbiAgICogU3BsaXQgYSBsb2NhbGUgaW50byBwYXJlbnQgbG9jYWxlcy4gXCJlcy1DT1wiIC0+IFtcImVzLUNPXCIsIFwiZXNcIl1cbiAgICpcbiAgICogQHBhcmFtIGxvY2FsZSAtIFRoZSBsb2NhbGUgc3RyaW5nLlxuICAgKlxuICAgKiBAcmV0dXJuIEFuIGFycmF5IG9mIGxvY2FsZXMuXG4gICAqL1xuICBwcml2YXRlIGV4cGFuZExvY2FsZShsb2NhbGU6IHN0cmluZyk6IEFycmF5PHN0cmluZz4ge1xuICAgIGxldCBsb2NhbGVzOiBBcnJheTxzdHJpbmc+ID0gW2xvY2FsZV07XG4gICAgbGV0IGk6IG51bWJlciA9IGxvY2FsZS5sYXN0SW5kZXhPZignLScpO1xuICAgIHdoaWxlIChpID4gMCkge1xuICAgICAgbG9jYWxlID0gbG9jYWxlLnNsaWNlKDAsIGkpO1xuICAgICAgbG9jYWxlcy5wdXNoKGxvY2FsZSk7XG4gICAgICBpID0gbG9jYWxlLmxhc3RJbmRleE9mKCctJyk7XG4gICAgfVxuICAgIHJldHVybiBsb2NhbGVzO1xuICB9XG5cbiAgLyoqXG4gICAqIFNwbGl0IGEgbG9jYWxlIGludG8gcGFyZW50IGxvY2FsZXMuIFwiZXMtQ09cIiAtPiBbXCJlcy1DT1wiLCBcImVzXCJdXG4gICAqXG4gICAqIEBwYXJhbSBwbHVyYWxGb3JtIC0gUGx1cmFsIGZvcm0gc3RyaW5nLi5cbiAgICogQHJldHVybiBBbiBmdW5jdGlvbiB0byBjb21wdXRlIHBsdXJhbCBmb3Jtcy5cbiAgICovXG4gIHByaXZhdGUgZ2V0UGx1cmFsRnVuYyhwbHVyYWxGb3JtOiBzdHJpbmcpOiBGdW5jdGlvbiB7XG4gICAgLy8gUGx1cmFsIGZvcm0gc3RyaW5nIHJlZ2V4cFxuICAgIC8vIHRha2VuIGZyb20gaHR0cHM6Ly9naXRodWIuY29tL09yYW5nZS1PcGVuU291cmNlL2dldHRleHQuanMvYmxvYi9tYXN0ZXIvbGliLmdldHRleHQuanNcbiAgICAvLyBwbHVyYWwgZm9ybXMgbGlzdCBhdmFpbGFibGUgaGVyZSBodHRwOi8vbG9jYWxpemF0aW9uLWd1aWRlLnJlYWR0aGVkb2NzLm9yZy9lbi9sYXRlc3QvbDEwbi9wbHVyYWxmb3Jtcy5odG1sXG4gICAgbGV0IHBmX3JlID0gbmV3IFJlZ0V4cChcbiAgICAgICdeXFxcXHMqbnBsdXJhbHNcXFxccyo9XFxcXHMqWzAtOV0rXFxcXHMqO1xcXFxzKnBsdXJhbFxcXFxzKj1cXFxccyooPzpcXFxcc3xbLVxcXFw/XFxcXHwmPSE8PisqLyU6O24wLTlfKCldKSsnXG4gICAgKTtcblxuICAgIGlmICghcGZfcmUudGVzdChwbHVyYWxGb3JtKSlcbiAgICAgIHRocm93IG5ldyBFcnJvcihcbiAgICAgICAgR2V0dGV4dC5zdHJmbXQoJ1RoZSBwbHVyYWwgZm9ybSBcIiUxXCIgaXMgbm90IHZhbGlkJywgcGx1cmFsRm9ybSlcbiAgICAgICk7XG5cbiAgICAvLyBDYXJlZnVsIGhlcmUsIHRoaXMgaXMgYSBoaWRkZW4gZXZhbCgpIGVxdWl2YWxlbnQuLlxuICAgIC8vIFJpc2sgc2hvdWxkIGJlIHJlYXNvbmFibGUgdGhvdWdoIHNpbmNlIHdlIHRlc3QgdGhlIHBsdXJhbEZvcm0gdGhyb3VnaCByZWdleCBiZWZvcmVcbiAgICAvLyB0YWtlbiBmcm9tIGh0dHBzOi8vZ2l0aHViLmNvbS9PcmFuZ2UtT3BlblNvdXJjZS9nZXR0ZXh0LmpzL2Jsb2IvbWFzdGVyL2xpYi5nZXR0ZXh0LmpzXG4gICAgLy8gVE9ETzogc2hvdWxkIHRlc3QgaWYgaHR0cHM6Ly9naXRodWIuY29tL3NvbmV5L2pzZXAgcHJlc2VudCBhbmQgdXNlIGl0IGlmIHNvXG4gICAgcmV0dXJuIG5ldyBGdW5jdGlvbihcbiAgICAgICduJyxcbiAgICAgICdsZXQgcGx1cmFsLCBucGx1cmFsczsgJyArXG4gICAgICAgIHBsdXJhbEZvcm0gK1xuICAgICAgICAnIHJldHVybiB7IG5wbHVyYWxzOiBucGx1cmFscywgcGx1cmFsOiAocGx1cmFsID09PSB0cnVlID8gMSA6IChwbHVyYWwgPyBwbHVyYWwgOiAwKSkgfTsnXG4gICAgKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW1vdmUgdGhlIGNvbnRleHQgZGVsaW1pdGVyIGZyb20gc3RyaW5nLlxuICAgKlxuICAgKiBAcGFyYW0gc3RyIC0gVHJhbnNsYXRpb24gc3RyaW5nLlxuICAgKiBAcmV0dXJuIEEgdHJhbnNsYXRpb24gc3RyaW5nIHdpdGhvdXQgY29udGV4dC5cbiAgICovXG4gIHByaXZhdGUgcmVtb3ZlQ29udGV4dChzdHI6IHN0cmluZyk6IHN0cmluZyB7XG4gICAgLy8gaWYgdGhlcmUgaXMgY29udGV4dCwgcmVtb3ZlIGl0XG4gICAgaWYgKHN0ci5pbmRleE9mKHRoaXMuX2NvbnRleHREZWxpbWl0ZXIpICE9PSAtMSkge1xuICAgICAgbGV0IHBhcnRzID0gc3RyLnNwbGl0KHRoaXMuX2NvbnRleHREZWxpbWl0ZXIpO1xuICAgICAgcmV0dXJuIHBhcnRzWzFdO1xuICAgIH1cbiAgICByZXR1cm4gc3RyO1xuICB9XG5cbiAgLyoqXG4gICAqIFByb3BlciB0cmFuc2xhdGlvbiBmdW5jdGlvbiB0aGF0IGhhbmRsZSBwbHVyYWxzIGFuZCBkaXJlY3RpdmVzLlxuICAgKlxuICAgKiBAcGFyYW0gbWVzc2FnZXMgLSBMaXN0IG9mIHRyYW5zbGF0aW9uIHN0cmluZ3MuXG4gICAqIEBwYXJhbSBuIC0gVGhlIG51bWJlciBmb3IgcGx1cmFsaXphdGlvbi5cbiAgICogQHBhcmFtIG9wdGlvbnMgLSBUcmFuc2xhdGlvbiBvcHRpb25zLlxuICAgKiBAcGFyYW0gYXJncyAtIEFueSB2YXJpYWJsZXMgdG8gaW50ZXJwb2xhdGUuXG4gICAqXG4gICAqIEByZXR1cm4gQSB0cmFuc2xhdGlvbiBzdHJpbmcgd2l0aG91dCBjb250ZXh0LlxuICAgKlxuICAgKiAjIyMgTm90ZXNcbiAgICogQ29udGFpbnMganVpY3kgcGFydHMgb2YgaHR0cHM6Ly9naXRodWIuY29tL09yYW5nZS1PcGVuU291cmNlL2dldHRleHQuanMvYmxvYi9tYXN0ZXIvbGliLmdldHRleHQuanNcbiAgICovXG4gIHByaXZhdGUgdChcbiAgICBtZXNzYWdlczogQXJyYXk8c3RyaW5nPixcbiAgICBuOiBudW1iZXIsXG4gICAgb3B0aW9uczogSVRPcHRpb25zLFxuICAgIC4uLmFyZ3M6IGFueVtdXG4gICk6IHN0cmluZyB7XG4gICAgLy8gU2luZ3VsYXIgaXMgdmVyeSBlYXN5LCBqdXN0IHBhc3MgZGljdGlvbmFyeSBtZXNzYWdlIHRocm91Z2ggc3RyZm10XG4gICAgaWYgKCFvcHRpb25zLnBsdXJhbEZvcm0pXG4gICAgICByZXR1cm4gKFxuICAgICAgICB0aGlzLl9zdHJpbmdzUHJlZml4ICtcbiAgICAgICAgR2V0dGV4dC5zdHJmbXQodGhpcy5yZW1vdmVDb250ZXh0KG1lc3NhZ2VzWzBdKSwgLi4uYXJncylcbiAgICAgICk7XG5cbiAgICBsZXQgcGx1cmFsO1xuXG4gICAgLy8gaWYgYSBwbHVyYWwgZnVuYyBpcyBnaXZlbiwgdXNlIHRoYXQgb25lXG4gICAgaWYgKG9wdGlvbnMucGx1cmFsRnVuYykge1xuICAgICAgcGx1cmFsID0gb3B0aW9ucy5wbHVyYWxGdW5jKG4pO1xuXG4gICAgICAvLyBpZiBwbHVyYWwgZm9ybSBuZXZlciBpbnRlcnByZXRlZCBiZWZvcmUsIGRvIGl0IG5vdyBhbmQgc3RvcmUgaXRcbiAgICB9IGVsc2UgaWYgKCF0aGlzLl9wbHVyYWxGdW5jc1tvcHRpb25zLmxvY2FsZSB8fCAnJ10pIHtcbiAgICAgIHRoaXMuX3BsdXJhbEZ1bmNzW29wdGlvbnMubG9jYWxlIHx8ICcnXSA9IHRoaXMuZ2V0UGx1cmFsRnVuYyhcbiAgICAgICAgdGhpcy5fcGx1cmFsRm9ybXNbb3B0aW9ucy5sb2NhbGUgfHwgJyddXG4gICAgICApO1xuICAgICAgcGx1cmFsID0gdGhpcy5fcGx1cmFsRnVuY3Nbb3B0aW9ucy5sb2NhbGUgfHwgJyddKG4pO1xuXG4gICAgICAvLyB3ZSBoYXZlIHRoZSBwbHVyYWwgZnVuY3Rpb24sIGNvbXB1dGUgdGhlIHBsdXJhbCByZXN1bHRcbiAgICB9IGVsc2Uge1xuICAgICAgcGx1cmFsID0gdGhpcy5fcGx1cmFsRnVuY3Nbb3B0aW9ucy5sb2NhbGUgfHwgJyddKG4pO1xuICAgIH1cblxuICAgIC8vIElmIHRoZXJlIGlzIGEgcHJvYmxlbSB3aXRoIHBsdXJhbHMsIGZhbGxiYWNrIHRvIHNpbmd1bGFyIG9uZVxuICAgIGlmIChcbiAgICAgICd1bmRlZmluZWQnID09PSB0eXBlb2YgIXBsdXJhbC5wbHVyYWwgfHxcbiAgICAgIHBsdXJhbC5wbHVyYWwgPiBwbHVyYWwubnBsdXJhbHMgfHxcbiAgICAgIG1lc3NhZ2VzLmxlbmd0aCA8PSBwbHVyYWwucGx1cmFsXG4gICAgKVxuICAgICAgcGx1cmFsLnBsdXJhbCA9IDA7XG5cbiAgICByZXR1cm4gKFxuICAgICAgdGhpcy5fc3RyaW5nc1ByZWZpeCArXG4gICAgICBHZXR0ZXh0LnN0cmZtdChcbiAgICAgICAgdGhpcy5yZW1vdmVDb250ZXh0KG1lc3NhZ2VzW3BsdXJhbC5wbHVyYWxdKSxcbiAgICAgICAgLi4uW25dLmNvbmNhdChhcmdzKVxuICAgICAgKVxuICAgICk7XG4gIH1cblxuICAvKipcbiAgICogU2V0IG1lc3NhZ2VzIGFmdGVyIGxvYWRpbmcgdGhlbS5cbiAgICpcbiAgICogQHBhcmFtIGRvbWFpbiAtIFRoZSB0cmFuc2xhdGlvbiBkb21haW4uXG4gICAqIEBwYXJhbSBsb2NhbGUgLSBUaGUgdHJhbnNsYXRpb24gbG9jYWxlLlxuICAgKiBAcGFyYW0gbWVzc2FnZXMgLSBMaXN0IG9mIHRyYW5zbGF0aW9uIHN0cmluZ3MuXG4gICAqIEBwYXJhbSBwbHVyYWxGb3JtcyAtIFBsdXJhbCBmb3JtIHN0cmluZy5cbiAgICpcbiAgICogIyMjIE5vdGVzXG4gICAqIENvbnRhaW5zIGp1aWN5IHBhcnRzIG9mIGh0dHBzOi8vZ2l0aHViLmNvbS9PcmFuZ2UtT3BlblNvdXJjZS9nZXR0ZXh0LmpzL2Jsb2IvbWFzdGVyL2xpYi5nZXR0ZXh0LmpzXG4gICAqL1xuICBwcml2YXRlIHNldE1lc3NhZ2VzKFxuICAgIGRvbWFpbjogc3RyaW5nLFxuICAgIGxvY2FsZTogc3RyaW5nLFxuICAgIG1lc3NhZ2VzOiBJSnNvbkRhdGFNZXNzYWdlcyxcbiAgICBwbHVyYWxGb3Jtczogc3RyaW5nXG4gICk6IHZvaWQge1xuICAgIGRvbWFpbiA9IG5vcm1hbGl6ZURvbWFpbihkb21haW4pO1xuXG4gICAgaWYgKHBsdXJhbEZvcm1zKSB0aGlzLl9wbHVyYWxGb3Jtc1tsb2NhbGVdID0gcGx1cmFsRm9ybXM7XG5cbiAgICBpZiAoIXRoaXMuX2RpY3Rpb25hcnlbZG9tYWluXSkgdGhpcy5fZGljdGlvbmFyeVtkb21haW5dID0ge307XG5cbiAgICB0aGlzLl9kaWN0aW9uYXJ5W2RvbWFpbl1bbG9jYWxlXSA9IG1lc3NhZ2VzO1xuICB9XG5cbiAgcHJpdmF0ZSBfc3RyaW5nc1ByZWZpeDogc3RyaW5nO1xuICBwcml2YXRlIF9wbHVyYWxGb3JtczogYW55O1xuICBwcml2YXRlIF9kaWN0aW9uYXJ5OiBhbnk7XG4gIHByaXZhdGUgX2xvY2FsZTogc3RyaW5nO1xuICBwcml2YXRlIF9kb21haW46IHN0cmluZztcbiAgcHJpdmF0ZSBfY29udGV4dERlbGltaXRlcjogc3RyaW5nO1xuICBwcml2YXRlIF9wbHVyYWxGdW5jczogYW55O1xuICBwcml2YXRlIF9kZWZhdWx0czogYW55O1xufVxuXG5leHBvcnQgeyBHZXR0ZXh0IH07XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSB0cmFuc2xhdGlvblxuICovXG5cbi8vIE5vdGU6IGtlZXAgaW4gYWxwaGFiZXRpY2FsIG9yZGVyLi4uXG5leHBvcnQgKiBmcm9tICcuL2Jhc2UnO1xuZXhwb3J0ICogZnJvbSAnLi9nZXR0ZXh0JztcbmV4cG9ydCAqIGZyb20gJy4vbWFuYWdlcic7XG5leHBvcnQgKiBmcm9tICcuL3NlcnZlcic7XG5leHBvcnQgKiBmcm9tICcuL3Rva2Vucyc7XG4iLCIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG5cbmltcG9ydCB7IFNlcnZlckNvbm5lY3Rpb24gfSBmcm9tICdAanVweXRlcmxhYi9zZXJ2aWNlcyc7XG5pbXBvcnQgeyBHZXR0ZXh0IH0gZnJvbSAnLi9nZXR0ZXh0JztcbmltcG9ydCB7IElUcmFuc2xhdG9yLCBUcmFuc2xhdGlvbkJ1bmRsZSwgVHJhbnNsYXRvckNvbm5lY3RvciB9IGZyb20gJy4vdG9rZW5zJztcbmltcG9ydCB7IG5vcm1hbGl6ZURvbWFpbiB9IGZyb20gJy4vdXRpbHMnO1xuXG4vKipcbiAqIFRyYW5zbGF0aW9uIE1hbmFnZXJcbiAqL1xuZXhwb3J0IGNsYXNzIFRyYW5zbGF0aW9uTWFuYWdlciBpbXBsZW1lbnRzIElUcmFuc2xhdG9yIHtcbiAgY29uc3RydWN0b3IoXG4gICAgdHJhbnNsYXRpb25zVXJsOiBzdHJpbmcgPSAnJyxcbiAgICBzdHJpbmdzUHJlZml4Pzogc3RyaW5nLFxuICAgIHNlcnZlclNldHRpbmdzPzogU2VydmVyQ29ubmVjdGlvbi5JU2V0dGluZ3NcbiAgKSB7XG4gICAgdGhpcy5fY29ubmVjdG9yID0gbmV3IFRyYW5zbGF0b3JDb25uZWN0b3IodHJhbnNsYXRpb25zVXJsLCBzZXJ2ZXJTZXR0aW5ncyk7XG4gICAgdGhpcy5fc3RyaW5nc1ByZWZpeCA9IHN0cmluZ3NQcmVmaXggfHwgJyc7XG4gICAgdGhpcy5fZW5nbGlzaEJ1bmRsZSA9IG5ldyBHZXR0ZXh0KHsgc3RyaW5nc1ByZWZpeDogdGhpcy5fc3RyaW5nc1ByZWZpeCB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBGZXRjaCB0aGUgbG9jYWxpemF0aW9uIGRhdGEgZnJvbSB0aGUgc2VydmVyLlxuICAgKlxuICAgKiBAcGFyYW0gbG9jYWxlIFRoZSBsYW5ndWFnZSBsb2NhbGUgdG8gdXNlIGZvciB0cmFuc2xhdGlvbnMuXG4gICAqL1xuICBhc3luYyBmZXRjaChsb2NhbGU6IHN0cmluZykge1xuICAgIHRoaXMuX2N1cnJlbnRMb2NhbGUgPSBsb2NhbGU7XG4gICAgdGhpcy5fbGFuZ3VhZ2VEYXRhID0gYXdhaXQgdGhpcy5fY29ubmVjdG9yLmZldGNoKHsgbGFuZ3VhZ2U6IGxvY2FsZSB9KTtcbiAgICB0aGlzLl9kb21haW5EYXRhID0gdGhpcy5fbGFuZ3VhZ2VEYXRhPy5kYXRhIHx8IHt9O1xuICAgIGNvbnN0IG1lc3NhZ2U6IHN0cmluZyA9IHRoaXMuX2xhbmd1YWdlRGF0YT8ubWVzc2FnZTtcbiAgICBpZiAobWVzc2FnZSAmJiBsb2NhbGUgIT09ICdlbicpIHtcbiAgICAgIGNvbnNvbGUud2FybihtZXNzYWdlKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogTG9hZCB0cmFuc2xhdGlvbiBidW5kbGVzIGZvciBhIGdpdmVuIGRvbWFpbi5cbiAgICpcbiAgICogQHBhcmFtIGRvbWFpbiBUaGUgdHJhbnNsYXRpb24gZG9tYWluIHRvIHVzZSBmb3IgdHJhbnNsYXRpb25zLlxuICAgKi9cbiAgbG9hZChkb21haW46IHN0cmluZyk6IFRyYW5zbGF0aW9uQnVuZGxlIHtcbiAgICBpZiAodGhpcy5fZG9tYWluRGF0YSkge1xuICAgICAgaWYgKHRoaXMuX2N1cnJlbnRMb2NhbGUgPT0gJ2VuJykge1xuICAgICAgICByZXR1cm4gdGhpcy5fZW5nbGlzaEJ1bmRsZTtcbiAgICAgIH0gZWxzZSB7XG4gICAgICAgIGRvbWFpbiA9IG5vcm1hbGl6ZURvbWFpbihkb21haW4pO1xuICAgICAgICBpZiAoIShkb21haW4gaW4gdGhpcy5fdHJhbnNsYXRpb25CdW5kbGVzKSkge1xuICAgICAgICAgIGxldCB0cmFuc2xhdGlvbkJ1bmRsZSA9IG5ldyBHZXR0ZXh0KHtcbiAgICAgICAgICAgIGRvbWFpbjogZG9tYWluLFxuICAgICAgICAgICAgbG9jYWxlOiB0aGlzLl9jdXJyZW50TG9jYWxlLFxuICAgICAgICAgICAgc3RyaW5nc1ByZWZpeDogdGhpcy5fc3RyaW5nc1ByZWZpeFxuICAgICAgICAgIH0pO1xuICAgICAgICAgIGlmIChkb21haW4gaW4gdGhpcy5fZG9tYWluRGF0YSkge1xuICAgICAgICAgICAgbGV0IG1ldGFkYXRhID0gdGhpcy5fZG9tYWluRGF0YVtkb21haW5dWycnXTtcbiAgICAgICAgICAgIGlmICgncGx1cmFsX2Zvcm1zJyBpbiBtZXRhZGF0YSkge1xuICAgICAgICAgICAgICBtZXRhZGF0YS5wbHVyYWxGb3JtcyA9IG1ldGFkYXRhLnBsdXJhbF9mb3JtcztcbiAgICAgICAgICAgICAgZGVsZXRlIG1ldGFkYXRhLnBsdXJhbF9mb3JtcztcbiAgICAgICAgICAgICAgdGhpcy5fZG9tYWluRGF0YVtkb21haW5dWycnXSA9IG1ldGFkYXRhO1xuICAgICAgICAgICAgfVxuICAgICAgICAgICAgdHJhbnNsYXRpb25CdW5kbGUubG9hZEpTT04odGhpcy5fZG9tYWluRGF0YVtkb21haW5dLCBkb21haW4pO1xuICAgICAgICAgIH1cbiAgICAgICAgICB0aGlzLl90cmFuc2xhdGlvbkJ1bmRsZXNbZG9tYWluXSA9IHRyYW5zbGF0aW9uQnVuZGxlO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiB0aGlzLl90cmFuc2xhdGlvbkJ1bmRsZXNbZG9tYWluXTtcbiAgICAgIH1cbiAgICB9IGVsc2Uge1xuICAgICAgcmV0dXJuIHRoaXMuX2VuZ2xpc2hCdW5kbGU7XG4gICAgfVxuICB9XG5cbiAgcHJpdmF0ZSBfY29ubmVjdG9yOiBUcmFuc2xhdG9yQ29ubmVjdG9yO1xuICBwcml2YXRlIF9jdXJyZW50TG9jYWxlOiBzdHJpbmc7XG4gIHByaXZhdGUgX2RvbWFpbkRhdGE6IGFueSA9IHt9O1xuICBwcml2YXRlIF9lbmdsaXNoQnVuZGxlOiBHZXR0ZXh0O1xuICBwcml2YXRlIF9sYW5ndWFnZURhdGE6IGFueTtcbiAgcHJpdmF0ZSBfc3RyaW5nc1ByZWZpeDogc3RyaW5nO1xuICBwcml2YXRlIF90cmFuc2xhdGlvbkJ1bmRsZXM6IGFueSA9IHt9O1xufVxuIiwiLy8gQ29weXJpZ2h0IChjKSBKdXB5dGVyIERldmVsb3BtZW50IFRlYW0uXG4vLyBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxuXG5pbXBvcnQgeyBVUkxFeHQgfSBmcm9tICdAanVweXRlcmxhYi9jb3JldXRpbHMnO1xuXG5pbXBvcnQgeyBTZXJ2ZXJDb25uZWN0aW9uIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2VydmljZXMnO1xuXG4vKipcbiAqIFRoZSB1cmwgZm9yIHRoZSB0cmFuc2xhdGlvbnMgc2VydmljZS5cbiAqL1xuY29uc3QgVFJBTlNMQVRJT05TX1NFVFRJTkdTX1VSTCA9ICdhcGkvdHJhbnNsYXRpb25zJztcblxuLyoqXG4gKiBDYWxsIHRoZSBBUEkgZXh0ZW5zaW9uXG4gKlxuICogQHBhcmFtIGxvY2FsZSBBUEkgUkVTVCBlbmQgcG9pbnQgZm9yIHRoZSBleHRlbnNpb25cbiAqIEBwYXJhbSBpbml0IEluaXRpYWwgdmFsdWVzIGZvciB0aGUgcmVxdWVzdFxuICogQHJldHVybnMgVGhlIHJlc3BvbnNlIGJvZHkgaW50ZXJwcmV0ZWQgYXMgSlNPTlxuICovXG5leHBvcnQgYXN5bmMgZnVuY3Rpb24gcmVxdWVzdFRyYW5zbGF0aW9uc0FQSTxUPihcbiAgdHJhbnNsYXRpb25zVXJsOiBzdHJpbmcgPSAnJyxcbiAgbG9jYWxlID0gJycsXG4gIGluaXQ6IFJlcXVlc3RJbml0ID0ge30sXG4gIHNlcnZlclNldHRpbmdzOiBTZXJ2ZXJDb25uZWN0aW9uLklTZXR0aW5ncyB8IHVuZGVmaW5lZCA9IHVuZGVmaW5lZFxuKTogUHJvbWlzZTxUPiB7XG4gIC8vIE1ha2UgcmVxdWVzdCB0byBKdXB5dGVyIEFQSVxuICBjb25zdCBzZXR0aW5ncyA9IHNlcnZlclNldHRpbmdzID8/IFNlcnZlckNvbm5lY3Rpb24ubWFrZVNldHRpbmdzKCk7XG4gIHRyYW5zbGF0aW9uc1VybCA9XG4gICAgdHJhbnNsYXRpb25zVXJsIHx8IGAke3NldHRpbmdzLmFwcFVybH0vJHtUUkFOU0xBVElPTlNfU0VUVElOR1NfVVJMfS9gO1xuICBjb25zdCByZXF1ZXN0VXJsID0gVVJMRXh0LmpvaW4oc2V0dGluZ3MuYmFzZVVybCwgdHJhbnNsYXRpb25zVXJsLCBsb2NhbGUpO1xuICBsZXQgcmVzcG9uc2U6IFJlc3BvbnNlO1xuICB0cnkge1xuICAgIHJlc3BvbnNlID0gYXdhaXQgU2VydmVyQ29ubmVjdGlvbi5tYWtlUmVxdWVzdChyZXF1ZXN0VXJsLCBpbml0LCBzZXR0aW5ncyk7XG4gIH0gY2F0Y2ggKGVycm9yKSB7XG4gICAgdGhyb3cgbmV3IFNlcnZlckNvbm5lY3Rpb24uTmV0d29ya0Vycm9yKGVycm9yKTtcbiAgfVxuXG4gIGxldCBkYXRhOiBhbnkgPSBhd2FpdCByZXNwb25zZS50ZXh0KCk7XG5cbiAgaWYgKGRhdGEubGVuZ3RoID4gMCkge1xuICAgIHRyeSB7XG4gICAgICBkYXRhID0gSlNPTi5wYXJzZShkYXRhKTtcbiAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgY29uc29sZS5lcnJvcignTm90IGEgSlNPTiByZXNwb25zZSBib2R5LicsIHJlc3BvbnNlKTtcbiAgICB9XG4gIH1cblxuICBpZiAoIXJlc3BvbnNlLm9rKSB7XG4gICAgdGhyb3cgbmV3IFNlcnZlckNvbm5lY3Rpb24uUmVzcG9uc2VFcnJvcihyZXNwb25zZSwgZGF0YS5tZXNzYWdlIHx8IGRhdGEpO1xuICB9XG5cbiAgcmV0dXJuIGRhdGE7XG59XG4iLCIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG58IENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxufCBEaXN0cmlidXRlZCB1bmRlciB0aGUgdGVybXMgb2YgdGhlIE1vZGlmaWVkIEJTRCBMaWNlbnNlLlxufC0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0qL1xuXG5pbXBvcnQgeyBTZXJ2ZXJDb25uZWN0aW9uIH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2VydmljZXMnO1xuaW1wb3J0IHsgRGF0YUNvbm5lY3RvciwgSURhdGFDb25uZWN0b3IgfSBmcm9tICdAanVweXRlcmxhYi9zdGF0ZWRiJztcbmltcG9ydCB7IFRva2VuIH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgcmVxdWVzdFRyYW5zbGF0aW9uc0FQSSB9IGZyb20gJy4vc2VydmVyJztcblxuLypcbiAqIFRyYW5zbGF0aW9uXG4gKi9cbnR5cGUgTGFuZ3VhZ2UgPSB7IFtrZXk6IHN0cmluZ106IHN0cmluZyB9O1xuXG5leHBvcnQgaW50ZXJmYWNlIElUcmFuc2xhdG9yQ29ubmVjdG9yXG4gIGV4dGVuZHMgSURhdGFDb25uZWN0b3I8TGFuZ3VhZ2UsIExhbmd1YWdlLCB7IGxhbmd1YWdlOiBzdHJpbmcgfT4ge31cblxuZXhwb3J0IGNvbnN0IElUcmFuc2xhdG9yQ29ubmVjdG9yID0gbmV3IFRva2VuPElUcmFuc2xhdG9yQ29ubmVjdG9yPihcbiAgJ0BqdXB5dGVybGFiL3RyYW5zbGF0aW9uOklUcmFuc2xhdG9yQ29ubmVjdG9yJ1xuKTtcblxuZXhwb3J0IGNsYXNzIFRyYW5zbGF0b3JDb25uZWN0b3JcbiAgZXh0ZW5kcyBEYXRhQ29ubmVjdG9yPExhbmd1YWdlLCBMYW5ndWFnZSwgeyBsYW5ndWFnZTogc3RyaW5nIH0+XG4gIGltcGxlbWVudHMgSVRyYW5zbGF0b3JDb25uZWN0b3Ige1xuICBjb25zdHJ1Y3RvcihcbiAgICB0cmFuc2xhdGlvbnNVcmw6IHN0cmluZyA9ICcnLFxuICAgIHNlcnZlclNldHRpbmdzPzogU2VydmVyQ29ubmVjdGlvbi5JU2V0dGluZ3NcbiAgKSB7XG4gICAgc3VwZXIoKTtcbiAgICB0aGlzLl90cmFuc2xhdGlvbnNVcmwgPSB0cmFuc2xhdGlvbnNVcmw7XG4gICAgdGhpcy5fc2VydmVyU2V0dGluZ3MgPSBzZXJ2ZXJTZXR0aW5ncztcbiAgfVxuXG4gIGFzeW5jIGZldGNoKG9wdHM6IHsgbGFuZ3VhZ2U6IHN0cmluZyB9KTogUHJvbWlzZTxMYW5ndWFnZT4ge1xuICAgIHJldHVybiByZXF1ZXN0VHJhbnNsYXRpb25zQVBJKFxuICAgICAgdGhpcy5fdHJhbnNsYXRpb25zVXJsLFxuICAgICAgb3B0cy5sYW5ndWFnZSxcbiAgICAgIHt9LFxuICAgICAgdGhpcy5fc2VydmVyU2V0dGluZ3NcbiAgICApO1xuICB9XG5cbiAgcHJpdmF0ZSBfc2VydmVyU2V0dGluZ3M6IFNlcnZlckNvbm5lY3Rpb24uSVNldHRpbmdzIHwgdW5kZWZpbmVkO1xuICBwcml2YXRlIF90cmFuc2xhdGlvbnNVcmw6IHN0cmluZztcbn1cblxuLyoqXG4gKiBCdW5kbGUgb2YgZ2V0dGV4dC1iYXNlZCB0cmFuc2xhdGlvbiBmdW5jdGlvbnMuXG4gKlxuICogVGhlIGNhbGxzIHRvIHRoZSBmdW5jdGlvbnMgaW4gdGhpcyBidW5kbGUgd2lsbCBiZSBhdXRvbWF0aWNhbGx5XG4gKiBleHRyYWN0ZWQgYnkgYGp1cHl0ZXJsYWItdHJhbnNsYXRlYCBwYWNrYWdlIHRvIGdlbmVyYXRlIHRyYW5zbGF0aW9uXG4gKiB0ZW1wbGF0ZSBmaWxlcyBpZiB0aGUgYnVuZGxlIGlzIGFzc2lnbmVkIHRvOlxuICogLSB2YXJpYWJsZSBuYW1lZCBgdHJhbnNgLFxuICogLSBwdWJsaWMgYXR0cmlidXRlIG5hbWVkIGB0cmFuc2AgKGB0aGlzLnRyYW5zYCksXG4gKiAtIHByaXZhdGUgYXR0cmlidXRlIG5hbWVkIGB0cmFuc2AgKGB0aGlzLl90cmFuc2ApLFxuICogLSBgdHJhbnNgIGF0dHJpYnV0ZSBgcHJvcHNgIHZhcmlhYmxlIChgcHJvcHMudHJhbnNgKSxcbiAqIC0gYHRyYW5zYCBhdHRyaWJ1dGUgYHByb3BzYCBhdHRyaWJ1dGUgKGB0aGlzLnByb3BzLnRyYW5zYClcbiAqL1xuZXhwb3J0IHR5cGUgVHJhbnNsYXRpb25CdW5kbGUgPSB7XG4gIC8qKlxuICAgKiBBbGlhcyBmb3IgYGdldHRleHRgICh0cmFuc2xhdGUgc3RyaW5ncyB3aXRob3V0IG51bWJlciBpbmZsZWN0aW9uKVxuICAgKiBAcGFyYW0gbXNnaWQgbWVzc2FnZSAodGV4dCB0byB0cmFuc2xhdGUpXG4gICAqIEBwYXJhbSBhcmdzXG4gICAqL1xuICBfXyhtc2dpZDogc3RyaW5nLCAuLi5hcmdzOiBhbnlbXSk6IHN0cmluZztcbiAgLyoqXG4gICAqIEFsaWFzIGZvciBgbmdldHRleHRgICh0cmFuc2xhdGUgYWNjb3VudGluZyBmb3IgcGx1cmFsIGZvcm1zKVxuICAgKiBAcGFyYW0gbXNnaWQgbWVzc2FnZSBmb3Igc2luZ3VsYXJcbiAgICogQHBhcmFtIG1zZ2lkX3BsdXJhbCBtZXNzYWdlIGZvciBwbHVyYWxcbiAgICogQHBhcmFtIG4gZGV0ZXJtaW5lcyB3aGljaCBwbHVyYWwgZm9ybSB0byB1c2VcbiAgICogQHBhcmFtIGFyZ3NcbiAgICovXG4gIF9uKG1zZ2lkOiBzdHJpbmcsIG1zZ2lkX3BsdXJhbDogc3RyaW5nLCBuOiBudW1iZXIsIC4uLmFyZ3M6IGFueVtdKTogc3RyaW5nO1xuICAvKipcbiAgICogQWxpYXMgZm9yIGBwZ2V0dGV4dGAgKHRyYW5zbGF0ZSBpbiBnaXZlbiBjb250ZXh0KVxuICAgKiBAcGFyYW0gbXNnY3R4dCBjb250ZXh0XG4gICAqIEBwYXJhbSBtc2dpZCBtZXNzYWdlICh0ZXh0IHRvIHRyYW5zbGF0ZSlcbiAgICogQHBhcmFtIGFyZ3NcbiAgICovXG4gIF9wKG1zZ2N0eHQ6IHN0cmluZywgbXNnaWQ6IHN0cmluZywgLi4uYXJnczogYW55W10pOiBzdHJpbmc7XG4gIC8qKlxuICAgKiBBbGlhcyBmb3IgYG5wZ2V0dGV4dGAgKHRyYW5zbGF0ZSBhY2NvdW50aW5nIGZvciBwbHVyYWwgZm9ybXMgaW4gZ2l2ZW4gY29udGV4dClcbiAgICogQHBhcmFtIG1zZ2N0eHQgY29udGV4dFxuICAgKiBAcGFyYW0gbXNnaWQgbWVzc2FnZSBmb3Igc2luZ3VsYXJcbiAgICogQHBhcmFtIG1zZ2lkX3BsdXJhbCBtZXNzYWdlIGZvciBwbHVyYWxcbiAgICogQHBhcmFtIG4gbnVtYmVyIHVzZWQgdG8gZGV0ZXJtaW5lIHdoaWNoIHBsdXJhbCBmb3JtIHRvIHVzZVxuICAgKiBAcGFyYW0gYXJnc1xuICAgKi9cbiAgX25wKFxuICAgIG1zZ2N0eHQ6IHN0cmluZyxcbiAgICBtc2dpZDogc3RyaW5nLFxuICAgIG1zZ2lkX3BsdXJhbDogc3RyaW5nLFxuICAgIG46IG51bWJlcixcbiAgICAuLi5hcmdzOiBhbnlbXVxuICApOiBzdHJpbmc7XG4gIGdldHRleHQobXNnaWQ6IHN0cmluZywgLi4uYXJnczogYW55W10pOiBzdHJpbmc7XG4gIG5nZXR0ZXh0KFxuICAgIG1zZ2lkOiBzdHJpbmcsXG4gICAgbXNnaWRfcGx1cmFsOiBzdHJpbmcsXG4gICAgbjogbnVtYmVyLFxuICAgIC4uLmFyZ3M6IGFueVtdXG4gICk6IHN0cmluZztcbiAgcGdldHRleHQobXNnY3R4dDogc3RyaW5nLCBtc2dpZDogc3RyaW5nLCAuLi5hcmdzOiBhbnlbXSk6IHN0cmluZztcbiAgbnBnZXR0ZXh0KFxuICAgIG1zZ2N0eHQ6IHN0cmluZyxcbiAgICBtc2dpZDogc3RyaW5nLFxuICAgIG1zZ2lkX3BsdXJhbDogc3RyaW5nLFxuICAgIG46IG51bWJlcixcbiAgICAuLi5hcmdzOiBhbnlbXVxuICApOiBzdHJpbmc7XG4gIGRjbnBnZXR0ZXh0KFxuICAgIGRvbWFpbjogc3RyaW5nLFxuICAgIG1zZ2N0eHQ6IHN0cmluZyxcbiAgICBtc2dpZDogc3RyaW5nLFxuICAgIG1zZ2lkX3BsdXJhbDogc3RyaW5nLFxuICAgIG46IG51bWJlcixcbiAgICAuLi5hcmdzOiBhbnlbXVxuICApOiBzdHJpbmc7XG59O1xuXG5leHBvcnQgaW50ZXJmYWNlIElUcmFuc2xhdG9yIHtcbiAgbG9hZChkb21haW46IHN0cmluZyk6IFRyYW5zbGF0aW9uQnVuZGxlO1xuICAvLyBsb2NhbGUoKTogc3RyaW5nO1xufVxuXG5leHBvcnQgY29uc3QgSVRyYW5zbGF0b3IgPSBuZXcgVG9rZW48SVRyYW5zbGF0b3I+KFxuICAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb246SVRyYW5zbGF0b3InXG4pO1xuIiwiLyoqXG4gKiBOb3JtYWxpemUgZG9tYWluXG4gKlxuICogQHBhcmFtIGRvbWFpbiBEb21haW4gdG8gbm9ybWFsaXplXG4gKiBAcmV0dXJucyBOb3JtYWxpemVkIGRvbWFpblxuICovXG5leHBvcnQgZnVuY3Rpb24gbm9ybWFsaXplRG9tYWluKGRvbWFpbjogc3RyaW5nKTogc3RyaW5nIHtcbiAgcmV0dXJuIGRvbWFpbi5yZXBsYWNlKCctJywgJ18nKTtcbn1cbiJdLCJzb3VyY2VSb290IjoiIn0=