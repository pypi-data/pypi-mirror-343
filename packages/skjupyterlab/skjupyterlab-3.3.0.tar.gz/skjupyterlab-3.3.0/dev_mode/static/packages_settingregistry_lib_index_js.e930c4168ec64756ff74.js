(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_settingregistry_lib_index_js"],{

/***/ "../packages/settingregistry/lib/index.js":
/*!************************************************!*\
  !*** ../packages/settingregistry/lib/index.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DefaultSchemaValidator": () => (/* reexport safe */ _settingregistry__WEBPACK_IMPORTED_MODULE_0__.DefaultSchemaValidator),
/* harmony export */   "SettingRegistry": () => (/* reexport safe */ _settingregistry__WEBPACK_IMPORTED_MODULE_0__.SettingRegistry),
/* harmony export */   "Settings": () => (/* reexport safe */ _settingregistry__WEBPACK_IMPORTED_MODULE_0__.Settings),
/* harmony export */   "ISettingRegistry": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry)
/* harmony export */ });
/* harmony import */ var _settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./settingregistry */ "../packages/settingregistry/lib/settingregistry.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./tokens */ "../packages/settingregistry/lib/tokens.js");
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/
/**
 * @packageDocumentation
 * @module settingregistry
 */




/***/ }),

/***/ "../packages/settingregistry/lib/settingregistry.js":
/*!**********************************************************!*\
  !*** ../packages/settingregistry/lib/settingregistry.js ***!
  \**********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DefaultSchemaValidator": () => (/* binding */ DefaultSchemaValidator),
/* harmony export */   "SettingRegistry": () => (/* binding */ SettingRegistry),
/* harmony export */   "Settings": () => (/* binding */ Settings)
/* harmony export */ });
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/commands */ "webpack/sharing/consume/default/@lumino/commands/@lumino/commands");
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_commands__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var ajv__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ajv */ "../node_modules/ajv/lib/ajv.js");
/* harmony import */ var ajv__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(ajv__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var json5__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! json5 */ "../node_modules/json5/dist/index.js");
/* harmony import */ var json5__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(json5__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _plugin_schema_json__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./plugin-schema.json */ "../packages/settingregistry/lib/plugin-schema.json");
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.







/**
 * An alias for the JSON deep copy function.
 */
const copy = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy;
/**
 * The default number of milliseconds before a `load()` call to the registry
 * will wait before timing out if it requires a transformation that has not been
 * registered.
 */
const DEFAULT_TRANSFORM_TIMEOUT = 1000;
/**
 * The ASCII record separator character.
 */
const RECORD_SEPARATOR = String.fromCharCode(30);
/**
 * The default implementation of a schema validator.
 */
class DefaultSchemaValidator {
    /**
     * Instantiate a schema validator.
     */
    constructor() {
        this._composer = new (ajv__WEBPACK_IMPORTED_MODULE_4___default())({ useDefaults: true });
        this._validator = new (ajv__WEBPACK_IMPORTED_MODULE_4___default())();
        this._composer.addSchema(_plugin_schema_json__WEBPACK_IMPORTED_MODULE_6__, 'jupyterlab-plugin-schema');
        this._validator.addSchema(_plugin_schema_json__WEBPACK_IMPORTED_MODULE_6__, 'jupyterlab-plugin-schema');
    }
    /**
     * Validate a plugin's schema and user data; populate the `composite` data.
     *
     * @param plugin - The plugin being validated. Its `composite` data will be
     * populated by reference.
     *
     * @param populate - Whether plugin data should be populated, defaults to
     * `true`.
     *
     * @return A list of errors if either the schema or data fail to validate or
     * `null` if there are no errors.
     */
    validateData(plugin, populate = true) {
        const validate = this._validator.getSchema(plugin.id);
        const compose = this._composer.getSchema(plugin.id);
        // If the schemas do not exist, add them to the validator and continue.
        if (!validate || !compose) {
            if (plugin.schema.type !== 'object') {
                const keyword = 'schema';
                const message = `Setting registry schemas' root-level type must be ` +
                    `'object', rejecting type: ${plugin.schema.type}`;
                return [{ dataPath: 'type', keyword, schemaPath: '', message }];
            }
            const errors = this._addSchema(plugin.id, plugin.schema);
            return errors || this.validateData(plugin);
        }
        // Parse the raw commented JSON into a user map.
        let user;
        try {
            user = json5__WEBPACK_IMPORTED_MODULE_5__.parse(plugin.raw);
        }
        catch (error) {
            if (error instanceof SyntaxError) {
                return [
                    {
                        dataPath: '',
                        keyword: 'syntax',
                        schemaPath: '',
                        message: error.message
                    }
                ];
            }
            const { column, description } = error;
            const line = error.lineNumber;
            return [
                {
                    dataPath: '',
                    keyword: 'parse',
                    schemaPath: '',
                    message: `${description} (line ${line} column ${column})`
                }
            ];
        }
        if (!validate(user)) {
            return validate.errors;
        }
        // Copy the user data before merging defaults into composite map.
        const composite = copy(user);
        if (!compose(composite)) {
            return compose.errors;
        }
        if (populate) {
            plugin.data = { composite, user };
        }
        return null;
    }
    /**
     * Add a schema to the validator.
     *
     * @param plugin - The plugin ID.
     *
     * @param schema - The schema being added.
     *
     * @return A list of errors if the schema fails to validate or `null` if there
     * are no errors.
     *
     * #### Notes
     * It is safe to call this function multiple times with the same plugin name.
     */
    _addSchema(plugin, schema) {
        const composer = this._composer;
        const validator = this._validator;
        const validate = validator.getSchema('jupyterlab-plugin-schema');
        // Validate against the main schema.
        if (!validate(schema)) {
            return validate.errors;
        }
        // Validate against the JSON schema meta-schema.
        if (!validator.validateSchema(schema)) {
            return validator.errors;
        }
        // Remove if schema already exists.
        composer.removeSchema(plugin);
        validator.removeSchema(plugin);
        // Add schema to the validator and composer.
        composer.addSchema(schema, plugin);
        validator.addSchema(schema, plugin);
        return null;
    }
}
/**
 * The default concrete implementation of a setting registry.
 */
class SettingRegistry {
    /**
     * Create a new setting registry.
     */
    constructor(options) {
        /**
         * The schema of the setting registry.
         */
        this.schema = _plugin_schema_json__WEBPACK_IMPORTED_MODULE_6__;
        /**
         * The collection of setting registry plugins.
         */
        this.plugins = Object.create(null);
        this._pluginChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this._ready = Promise.resolve();
        this._transformers = Object.create(null);
        this.connector = options.connector;
        this.validator = options.validator || new DefaultSchemaValidator();
        this._timeout = options.timeout || DEFAULT_TRANSFORM_TIMEOUT;
        // Preload with any available data at instantiation-time.
        if (options.plugins) {
            this._ready = this._preload(options.plugins);
        }
    }
    /**
     * A signal that emits the name of a plugin when its settings change.
     */
    get pluginChanged() {
        return this._pluginChanged;
    }
    /**
     * Get an individual setting.
     *
     * @param plugin - The name of the plugin whose settings are being retrieved.
     *
     * @param key - The name of the setting being retrieved.
     *
     * @returns A promise that resolves when the setting is retrieved.
     */
    async get(plugin, key) {
        // Wait for data preload before allowing normal operation.
        await this._ready;
        const plugins = this.plugins;
        if (plugin in plugins) {
            const { composite, user } = plugins[plugin].data;
            return {
                composite: composite[key] !== undefined ? copy(composite[key]) : undefined,
                user: user[key] !== undefined ? copy(user[key]) : undefined
            };
        }
        return this.load(plugin).then(() => this.get(plugin, key));
    }
    /**
     * Load a plugin's settings into the setting registry.
     *
     * @param plugin - The name of the plugin whose settings are being loaded.
     *
     * @returns A promise that resolves with a plugin settings object or rejects
     * if the plugin is not found.
     */
    async load(plugin) {
        // Wait for data preload before allowing normal operation.
        await this._ready;
        const plugins = this.plugins;
        const registry = this; // eslint-disable-line
        // If the plugin exists, resolve.
        if (plugin in plugins) {
            return new Settings({ plugin: plugins[plugin], registry });
        }
        // If the plugin needs to be loaded from the data connector, fetch.
        return this.reload(plugin);
    }
    /**
     * Reload a plugin's settings into the registry even if they already exist.
     *
     * @param plugin - The name of the plugin whose settings are being reloaded.
     *
     * @returns A promise that resolves with a plugin settings object or rejects
     * with a list of `ISchemaValidator.IError` objects if it fails.
     */
    async reload(plugin) {
        // Wait for data preload before allowing normal operation.
        await this._ready;
        const fetched = await this.connector.fetch(plugin);
        const plugins = this.plugins; // eslint-disable-line
        const registry = this; // eslint-disable-line
        if (fetched === undefined) {
            throw [
                {
                    dataPath: '',
                    keyword: 'id',
                    message: `Could not fetch settings for ${plugin}.`,
                    schemaPath: ''
                }
            ];
        }
        await this._load(await this._transform('fetch', fetched));
        this._pluginChanged.emit(plugin);
        return new Settings({ plugin: plugins[plugin], registry });
    }
    /**
     * Remove a single setting in the registry.
     *
     * @param plugin - The name of the plugin whose setting is being removed.
     *
     * @param key - The name of the setting being removed.
     *
     * @returns A promise that resolves when the setting is removed.
     */
    async remove(plugin, key) {
        // Wait for data preload before allowing normal operation.
        await this._ready;
        const plugins = this.plugins;
        if (!(plugin in plugins)) {
            return;
        }
        const raw = json5__WEBPACK_IMPORTED_MODULE_5__.parse(plugins[plugin].raw);
        // Delete both the value and any associated comment.
        delete raw[key];
        delete raw[`// ${key}`];
        plugins[plugin].raw = Private.annotatedPlugin(plugins[plugin], raw);
        return this._save(plugin);
    }
    /**
     * Set a single setting in the registry.
     *
     * @param plugin - The name of the plugin whose setting is being set.
     *
     * @param key - The name of the setting being set.
     *
     * @param value - The value of the setting being set.
     *
     * @returns A promise that resolves when the setting has been saved.
     *
     */
    async set(plugin, key, value) {
        // Wait for data preload before allowing normal operation.
        await this._ready;
        const plugins = this.plugins;
        if (!(plugin in plugins)) {
            return this.load(plugin).then(() => this.set(plugin, key, value));
        }
        // Parse the raw JSON string removing all comments and return an object.
        const raw = json5__WEBPACK_IMPORTED_MODULE_5__.parse(plugins[plugin].raw);
        plugins[plugin].raw = Private.annotatedPlugin(plugins[plugin], Object.assign(Object.assign({}, raw), { [key]: value }));
        return this._save(plugin);
    }
    /**
     * Register a plugin transform function to act on a specific plugin.
     *
     * @param plugin - The name of the plugin whose settings are transformed.
     *
     * @param transforms - The transform functions applied to the plugin.
     *
     * @returns A disposable that removes the transforms from the registry.
     *
     * #### Notes
     * - `compose` transformations: The registry automatically overwrites a
     * plugin's default values with user overrides, but a plugin may instead wish
     * to merge values. This behavior can be accomplished in a `compose`
     * transformation.
     * - `fetch` transformations: The registry uses the plugin data that is
     * fetched from its connector. If a plugin wants to override, e.g. to update
     * its schema with dynamic defaults, a `fetch` transformation can be applied.
     */
    transform(plugin, transforms) {
        const transformers = this._transformers;
        if (plugin in transformers) {
            throw new Error(`${plugin} already has a transformer.`);
        }
        transformers[plugin] = {
            fetch: transforms.fetch || (plugin => plugin),
            compose: transforms.compose || (plugin => plugin)
        };
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_2__.DisposableDelegate(() => {
            delete transformers[plugin];
        });
    }
    /**
     * Upload a plugin's settings.
     *
     * @param plugin - The name of the plugin whose settings are being set.
     *
     * @param raw - The raw plugin settings being uploaded.
     *
     * @returns A promise that resolves when the settings have been saved.
     */
    async upload(plugin, raw) {
        // Wait for data preload before allowing normal operation.
        await this._ready;
        const plugins = this.plugins;
        if (!(plugin in plugins)) {
            return this.load(plugin).then(() => this.upload(plugin, raw));
        }
        // Set the local copy.
        plugins[plugin].raw = raw;
        return this._save(plugin);
    }
    /**
     * Load a plugin into the registry.
     */
    async _load(data) {
        const plugin = data.id;
        // Validate and preload the item.
        try {
            await this._validate(data);
        }
        catch (errors) {
            const output = [`Validating ${plugin} failed:`];
            errors.forEach((error, index) => {
                const { dataPath, schemaPath, keyword, message } = error;
                if (dataPath || schemaPath) {
                    output.push(`${index} - schema @ ${schemaPath}, data @ ${dataPath}`);
                }
                output.push(`{${keyword}} ${message}`);
            });
            console.warn(output.join('\n'));
            throw errors;
        }
    }
    /**
     * Preload a list of plugins and fail gracefully.
     */
    async _preload(plugins) {
        await Promise.all(plugins.map(async (plugin) => {
            var _a;
            try {
                // Apply a transformation to the plugin if necessary.
                await this._load(await this._transform('fetch', plugin));
            }
            catch (errors) {
                /* Ignore preload timeout errors silently. */
                if (((_a = errors[0]) === null || _a === void 0 ? void 0 : _a.keyword) !== 'timeout') {
                    console.warn('Ignored setting registry preload errors.', errors);
                }
            }
        }));
    }
    /**
     * Save a plugin in the registry.
     */
    async _save(plugin) {
        const plugins = this.plugins;
        if (!(plugin in plugins)) {
            throw new Error(`${plugin} does not exist in setting registry.`);
        }
        try {
            await this._validate(plugins[plugin]);
        }
        catch (errors) {
            console.warn(`${plugin} validation errors:`, errors);
            throw new Error(`${plugin} failed to validate; check console.`);
        }
        await this.connector.save(plugin, plugins[plugin].raw);
        // Fetch and reload the data to guarantee server and client are in sync.
        const fetched = await this.connector.fetch(plugin);
        if (fetched === undefined) {
            throw [
                {
                    dataPath: '',
                    keyword: 'id',
                    message: `Could not fetch settings for ${plugin}.`,
                    schemaPath: ''
                }
            ];
        }
        await this._load(await this._transform('fetch', fetched));
        this._pluginChanged.emit(plugin);
    }
    /**
     * Transform the plugin if necessary.
     */
    async _transform(phase, plugin, started = new Date().getTime()) {
        const elapsed = new Date().getTime() - started;
        const id = plugin.id;
        const transformers = this._transformers;
        const timeout = this._timeout;
        if (!plugin.schema['jupyter.lab.transform']) {
            return plugin;
        }
        if (id in transformers) {
            const transformed = transformers[id][phase].call(null, plugin);
            if (transformed.id !== id) {
                throw [
                    {
                        dataPath: '',
                        keyword: 'id',
                        message: 'Plugin transformations cannot change plugin IDs.',
                        schemaPath: ''
                    }
                ];
            }
            return transformed;
        }
        // If the timeout has not been exceeded, stall and try again in 250ms.
        if (elapsed < timeout) {
            await new Promise(resolve => {
                setTimeout(() => {
                    resolve();
                }, 250);
            });
            return this._transform(phase, plugin, started);
        }
        throw [
            {
                dataPath: '',
                keyword: 'timeout',
                message: `Transforming ${plugin.id} timed out.`,
                schemaPath: ''
            }
        ];
    }
    /**
     * Validate and preload a plugin, compose the `composite` data.
     */
    async _validate(plugin) {
        // Validate the user data and create the composite data.
        const errors = this.validator.validateData(plugin);
        if (errors) {
            throw errors;
        }
        // Apply a transformation if necessary and set the local copy.
        this.plugins[plugin.id] = await this._transform('compose', plugin);
    }
}
/**
 * A manager for a specific plugin's settings.
 */
class Settings {
    /**
     * Instantiate a new plugin settings manager.
     */
    constructor(options) {
        this._changed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal(this);
        this._isDisposed = false;
        this.id = options.plugin.id;
        this.registry = options.registry;
        this.registry.pluginChanged.connect(this._onPluginChanged, this);
    }
    /**
     * A signal that emits when the plugin's settings have changed.
     */
    get changed() {
        return this._changed;
    }
    /**
     * The composite of user settings and extension defaults.
     */
    get composite() {
        return this.plugin.data.composite;
    }
    /**
     * Test whether the plugin settings manager disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    get plugin() {
        return this.registry.plugins[this.id];
    }
    /**
     * The plugin's schema.
     */
    get schema() {
        return this.plugin.schema;
    }
    /**
     * The plugin settings raw text value.
     */
    get raw() {
        return this.plugin.raw;
    }
    /**
     * The user settings.
     */
    get user() {
        return this.plugin.data.user;
    }
    /**
     * The published version of the NPM package containing these settings.
     */
    get version() {
        return this.plugin.version;
    }
    /**
     * Return the defaults in a commented JSON format.
     */
    annotatedDefaults() {
        return Private.annotatedDefaults(this.schema, this.id);
    }
    /**
     * Calculate the default value of a setting by iterating through the schema.
     *
     * @param key - The name of the setting whose default value is calculated.
     *
     * @returns A calculated default JSON value for a specific setting.
     */
    default(key) {
        return Private.reifyDefault(this.schema, key);
    }
    /**
     * Dispose of the plugin settings resources.
     */
    dispose() {
        if (this._isDisposed) {
            return;
        }
        this._isDisposed = true;
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_3__.Signal.clearData(this);
    }
    /**
     * Get an individual setting.
     *
     * @param key - The name of the setting being retrieved.
     *
     * @returns The setting value.
     *
     * #### Notes
     * This method returns synchronously because it uses a cached copy of the
     * plugin settings that is synchronized with the registry.
     */
    get(key) {
        const { composite, user } = this;
        return {
            composite: composite[key] !== undefined ? copy(composite[key]) : undefined,
            user: user[key] !== undefined ? copy(user[key]) : undefined
        };
    }
    /**
     * Remove a single setting.
     *
     * @param key - The name of the setting being removed.
     *
     * @returns A promise that resolves when the setting is removed.
     *
     * #### Notes
     * This function is asynchronous because it writes to the setting registry.
     */
    remove(key) {
        return this.registry.remove(this.plugin.id, key);
    }
    /**
     * Save all of the plugin's user settings at once.
     */
    save(raw) {
        return this.registry.upload(this.plugin.id, raw);
    }
    /**
     * Set a single setting.
     *
     * @param key - The name of the setting being set.
     *
     * @param value - The value of the setting.
     *
     * @returns A promise that resolves when the setting has been saved.
     *
     * #### Notes
     * This function is asynchronous because it writes to the setting registry.
     */
    set(key, value) {
        return this.registry.set(this.plugin.id, key, value);
    }
    /**
     * Validates raw settings with comments.
     *
     * @param raw - The JSON with comments string being validated.
     *
     * @returns A list of errors or `null` if valid.
     */
    validate(raw) {
        const data = { composite: {}, user: {} };
        const { id, schema } = this.plugin;
        const validator = this.registry.validator;
        const version = this.version;
        return validator.validateData({ data, id, raw, schema, version }, false);
    }
    /**
     * Handle plugin changes in the setting registry.
     */
    _onPluginChanged(sender, plugin) {
        if (plugin === this.plugin.id) {
            this._changed.emit(undefined);
        }
    }
}
/**
 * A namespace for `SettingRegistry` statics.
 */
(function (SettingRegistry) {
    /**
     * Reconcile the menus.
     *
     * @param reference The reference list of menus.
     * @param addition The list of menus to add.
     * @param warn Warn if the command items are duplicated within the same menu.
     * @returns The reconciled list of menus.
     */
    function reconcileMenus(reference, addition, warn = false, addNewItems = true) {
        if (!reference) {
            return addition && addNewItems ? _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(addition) : [];
        }
        if (!addition) {
            return _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(reference);
        }
        const merged = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(reference);
        addition.forEach(menu => {
            const refIndex = merged.findIndex(ref => ref.id === menu.id);
            if (refIndex >= 0) {
                merged[refIndex] = Object.assign(Object.assign(Object.assign({}, merged[refIndex]), menu), { items: reconcileItems(merged[refIndex].items, menu.items, warn, addNewItems) });
            }
            else {
                if (addNewItems) {
                    merged.push(menu);
                }
            }
        });
        return merged;
    }
    SettingRegistry.reconcileMenus = reconcileMenus;
    /**
     * Merge two set of menu items.
     *
     * @param reference Reference set of menu items
     * @param addition New items to add
     * @param warn Whether to warn if item is duplicated; default to false
     * @returns The merged set of items
     */
    function reconcileItems(reference, addition, warn = false, addNewItems = true) {
        if (!reference) {
            return addition ? _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(addition) : undefined;
        }
        if (!addition) {
            return _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(reference);
        }
        const items = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(reference);
        // Merge array element depending on the type
        addition.forEach(item => {
            var _a;
            switch ((_a = item.type) !== null && _a !== void 0 ? _a : 'command') {
                case 'separator':
                    if (addNewItems) {
                        items.push(Object.assign({}, item));
                    }
                    break;
                case 'submenu':
                    if (item.submenu) {
                        const refIndex = items.findIndex(ref => { var _a, _b; return ref.type === 'submenu' && ((_a = ref.submenu) === null || _a === void 0 ? void 0 : _a.id) === ((_b = item.submenu) === null || _b === void 0 ? void 0 : _b.id); });
                        if (refIndex < 0) {
                            if (addNewItems) {
                                items.push(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(item));
                            }
                        }
                        else {
                            items[refIndex] = Object.assign(Object.assign(Object.assign({}, items[refIndex]), item), { submenu: reconcileMenus(items[refIndex].submenu
                                    ? [items[refIndex].submenu]
                                    : null, [item.submenu], warn, addNewItems)[0] });
                        }
                    }
                    break;
                case 'command':
                    if (item.command) {
                        const refIndex = items.findIndex(ref => {
                            var _a, _b;
                            return ref.command === item.command &&
                                ref.selector === item.selector &&
                                _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepEqual((_a = ref.args) !== null && _a !== void 0 ? _a : {}, (_b = item.args) !== null && _b !== void 0 ? _b : {});
                        });
                        if (refIndex < 0) {
                            if (addNewItems) {
                                items.push(Object.assign({}, item));
                            }
                        }
                        else {
                            if (warn) {
                                console.warn(`Menu entry for command '${item.command}' is duplicated.`);
                            }
                            items[refIndex] = Object.assign(Object.assign({}, items[refIndex]), item);
                        }
                    }
            }
        });
        return items;
    }
    SettingRegistry.reconcileItems = reconcileItems;
    function filterDisabledItems(items) {
        return items.reduce((final, value) => {
            var _a;
            const copy = Object.assign({}, value);
            if (!copy.disabled) {
                if (copy.type === 'submenu') {
                    const { submenu } = copy;
                    if (submenu && !submenu.disabled) {
                        copy.submenu = Object.assign(Object.assign({}, submenu), { items: filterDisabledItems((_a = submenu.items) !== null && _a !== void 0 ? _a : []) });
                    }
                }
                final.push(copy);
            }
            return final;
        }, []);
    }
    SettingRegistry.filterDisabledItems = filterDisabledItems;
    /**
     * Reconcile default and user shortcuts and return the composite list.
     *
     * @param defaults - The list of default shortcuts.
     *
     * @param user - The list of user shortcut overrides and additions.
     *
     * @returns A loadable list of shortcuts (omitting disabled and overridden).
     */
    function reconcileShortcuts(defaults, user) {
        const memo = {};
        // If a user shortcut collides with another user shortcut warn and filter.
        user = user.filter(shortcut => {
            const keys = _lumino_commands__WEBPACK_IMPORTED_MODULE_0__.CommandRegistry.normalizeKeys(shortcut).join(RECORD_SEPARATOR);
            if (!keys) {
                console.warn('Skipping this shortcut because there are no actionable keys on this platform', shortcut);
                return false;
            }
            if (!(keys in memo)) {
                memo[keys] = {};
            }
            const { selector } = shortcut;
            if (!(selector in memo[keys])) {
                memo[keys][selector] = false; // Do not warn if a default shortcut conflicts.
                return true;
            }
            console.warn('Skipping this shortcut because it collides with another shortcut.', shortcut);
            return false;
        });
        // If a default shortcut collides with another default, warn and filter,
        // unless one of the shortcuts is a disabling shortcut (so look through
        // disabled shortcuts first). If a shortcut has already been added by the
        // user preferences, filter it out too (this includes shortcuts that are
        // disabled by user preferences).
        defaults = [
            ...defaults.filter(s => !!s.disabled),
            ...defaults.filter(s => !s.disabled)
        ].filter(shortcut => {
            const keys = _lumino_commands__WEBPACK_IMPORTED_MODULE_0__.CommandRegistry.normalizeKeys(shortcut).join(RECORD_SEPARATOR);
            if (!keys) {
                return false;
            }
            if (!(keys in memo)) {
                memo[keys] = {};
            }
            const { disabled, selector } = shortcut;
            if (!(selector in memo[keys])) {
                // Warn of future conflicts if the default shortcut is not disabled.
                memo[keys][selector] = !disabled;
                return true;
            }
            // We have a conflict now. Warn the user if we need to do so.
            if (memo[keys][selector]) {
                console.warn('Skipping this default shortcut because it collides with another default shortcut.', shortcut);
            }
            return false;
        });
        // Return all the shortcuts that should be registered
        return user.concat(defaults).filter(shortcut => !shortcut.disabled);
    }
    SettingRegistry.reconcileShortcuts = reconcileShortcuts;
})(SettingRegistry || (SettingRegistry = {}));
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * The default indentation level, uses spaces instead of tabs.
     */
    const indent = '    ';
    /**
     * Replacement text for schema properties missing a `description` field.
     */
    const nondescript = '[missing schema description]';
    /**
     * Replacement text for schema properties missing a `title` field.
     */
    const untitled = '[missing schema title]';
    /**
     * Returns an annotated (JSON with comments) version of a schema's defaults.
     */
    function annotatedDefaults(schema, plugin) {
        const { description, properties, title } = schema;
        const keys = properties
            ? Object.keys(properties).sort((a, b) => a.localeCompare(b))
            : [];
        const length = Math.max((description || nondescript).length, plugin.length);
        return [
            '{',
            prefix(`${title || untitled}`),
            prefix(plugin),
            prefix(description || nondescript),
            prefix('*'.repeat(length)),
            '',
            join(keys.map(key => defaultDocumentedValue(schema, key))),
            '}'
        ].join('\n');
    }
    Private.annotatedDefaults = annotatedDefaults;
    /**
     * Returns an annotated (JSON with comments) version of a plugin's
     * setting data.
     */
    function annotatedPlugin(plugin, data) {
        const { description, title } = plugin.schema;
        const keys = Object.keys(data).sort((a, b) => a.localeCompare(b));
        const length = Math.max((description || nondescript).length, plugin.id.length);
        return [
            '{',
            prefix(`${title || untitled}`),
            prefix(plugin.id),
            prefix(description || nondescript),
            prefix('*'.repeat(length)),
            '',
            join(keys.map(key => documentedValue(plugin.schema, key, data[key]))),
            '}'
        ].join('\n');
    }
    Private.annotatedPlugin = annotatedPlugin;
    /**
     * Returns the default value-with-documentation-string for a
     * specific schema property.
     */
    function defaultDocumentedValue(schema, key) {
        const props = (schema.properties && schema.properties[key]) || {};
        const type = props['type'];
        const description = props['description'] || nondescript;
        const title = props['title'] || '';
        const reified = reifyDefault(schema, key);
        const spaces = indent.length;
        const defaults = reified !== undefined
            ? prefix(`"${key}": ${JSON.stringify(reified, null, spaces)}`, indent)
            : prefix(`"${key}": ${type}`);
        return [prefix(title), prefix(description), defaults]
            .filter(str => str.length)
            .join('\n');
    }
    /**
     * Returns a value-with-documentation-string for a specific schema property.
     */
    function documentedValue(schema, key, value) {
        const props = schema.properties && schema.properties[key];
        const description = (props && props['description']) || nondescript;
        const title = (props && props['title']) || untitled;
        const spaces = indent.length;
        const attribute = prefix(`"${key}": ${JSON.stringify(value, null, spaces)}`, indent);
        return [prefix(title), prefix(description), attribute].join('\n');
    }
    /**
     * Returns a joined string with line breaks and commas where appropriate.
     */
    function join(body) {
        return body.reduce((acc, val, idx) => {
            const rows = val.split('\n');
            const last = rows[rows.length - 1];
            const comment = last.trim().indexOf('//') === 0;
            const comma = comment || idx === body.length - 1 ? '' : ',';
            const separator = idx === body.length - 1 ? '' : '\n\n';
            return acc + val + comma + separator;
        }, '');
    }
    /**
     * Returns a documentation string with a comment prefix added on every line.
     */
    function prefix(source, pre = `${indent}// `) {
        return pre + source.split('\n').join(`\n${pre}`);
    }
    /**
     * Create a fully extrapolated default value for a root key in a schema.
     */
    function reifyDefault(schema, root) {
        var _a;
        // If the property is at the root level, traverse its schema.
        schema = (root ? (_a = schema.properties) === null || _a === void 0 ? void 0 : _a[root] : schema) || {};
        // If the property has no default or is a primitive, return.
        if (!('default' in schema) || schema.type !== 'object') {
            return schema.default;
        }
        // Make a copy of the default value to populate.
        const result = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.JSONExt.deepCopy(schema.default);
        // Iterate through and populate each child property.
        const props = schema.properties || {};
        for (const property in props) {
            result[property] = reifyDefault(props[property]);
        }
        return result;
    }
    Private.reifyDefault = reifyDefault;
})(Private || (Private = {}));


/***/ }),

/***/ "../packages/settingregistry/lib/tokens.js":
/*!*************************************************!*\
  !*** ../packages/settingregistry/lib/tokens.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ISettingRegistry": () => (/* binding */ ISettingRegistry)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* -----------------------------------------------------------------------------
| Copyright (c) Jupyter Development Team.
| Distributed under the terms of the Modified BSD License.
|----------------------------------------------------------------------------*/

/* tslint:disable */
/**
 * The setting registry token.
 */
const ISettingRegistry = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/coreutils:ISettingRegistry');


/***/ }),

/***/ "../packages/settingregistry/lib/plugin-schema.json":
/*!**********************************************************!*\
  !*** ../packages/settingregistry/lib/plugin-schema.json ***!
  \**********************************************************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"$schema":"http://json-schema.org/draft-07/schema","title":"JupyterLab Plugin Settings/Preferences Schema","description":"JupyterLab plugin settings/preferences schema","version":"1.0.0","type":"object","additionalProperties":true,"properties":{"jupyter.lab.internationalization":{"type":"object","properties":{"selectors":{"type":"array","items":{"type":"string","minLength":1}},"domain":{"type":"string","minLength":1}}},"jupyter.lab.menus":{"type":"object","properties":{"main":{"title":"Main menu entries","description":"List of menu items to add to the main menubar.","items":{"$ref":"#/definitions/menu"},"type":"array","default":[]},"context":{"title":"The application context menu.","description":"List of context menu items.","items":{"allOf":[{"$ref":"#/definitions/menuItem"},{"properties":{"selector":{"description":"The CSS selector for the context menu item.","type":"string"}}}]},"type":"array","default":[]}},"additionalProperties":false},"jupyter.lab.setting-deprecated":{"type":"boolean","default":false},"jupyter.lab.setting-icon":{"type":"string","default":""},"jupyter.lab.setting-icon-class":{"type":"string","default":""},"jupyter.lab.setting-icon-label":{"type":"string","default":"Plugin"},"jupyter.lab.shortcuts":{"items":{"$ref":"#/definitions/shortcut"},"type":"array","default":[]},"jupyter.lab.transform":{"type":"boolean","default":false}},"definitions":{"menu":{"properties":{"disabled":{"description":"Whether the menu is disabled or not","type":"boolean","default":false},"icon":{"description":"Menu icon id","type":"string"},"id":{"description":"Menu unique id","oneOf":[{"type":"string","enum":["jp-menu-file","jp-menu-file-new","jp-menu-edit","jp-menu-help","jp-menu-kernel","jp-menu-run","jp-menu-settings","jp-menu-view","jp-menu-tabs"]},{"type":"string","pattern":"[a-z][a-z0-9\\\\-_]+"}]},"items":{"description":"Menu items","type":"array","items":{"$ref":"#/definitions/menuItem"}},"label":{"description":"Menu label","type":"string"},"mnemonic":{"description":"Mnemonic index for the label","type":"number","minimum":-1,"default":-1},"rank":{"description":"Menu rank","type":"number","minimum":0}},"required":["id"],"type":"object"},"menuItem":{"properties":{"args":{"description":"Command arguments","type":"object"},"command":{"description":"Command id","type":"string"},"disabled":{"description":"Whether the item is disabled or not","type":"boolean","default":false},"type":{"description":"Item type","type":"string","enum":["command","submenu","separator"],"default":"command"},"rank":{"description":"Item rank","type":"number","minimum":0},"submenu":{"oneOf":[{"$ref":"#/definitions/menu"},{"type":"null"}]}},"type":"object"},"shortcut":{"properties":{"args":{"type":"object"},"command":{"type":"string"},"disabled":{"type":"boolean","default":false},"keys":{"items":{"type":"string"},"minItems":1,"type":"array"},"selector":{"type":"string"}},"required":["command","keys","selector"],"type":"object"}}}');

/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc2V0dGluZ3JlZ2lzdHJ5L3NyYy9pbmRleC50cyIsIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc2V0dGluZ3JlZ2lzdHJ5L3NyYy9zZXR0aW5ncmVnaXN0cnkudHMiLCJ3ZWJwYWNrOi8vQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24tdG9wLy4uL3BhY2thZ2VzL3NldHRpbmdyZWdpc3RyeS9zcmMvdG9rZW5zLnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQUFBOzs7K0VBRytFO0FBQy9FOzs7R0FHRztBQUUrQjtBQUNUOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDVnpCLDBDQUEwQztBQUMxQywyREFBMkQ7QUFHUjtBQVV4QjtBQUMwQztBQUNqQjtBQUM5QjtBQUNTO0FBQ1c7QUFHMUM7O0dBRUc7QUFDSCxNQUFNLElBQUksR0FBRywrREFBZ0IsQ0FBQztBQUU5Qjs7OztHQUlHO0FBQ0gsTUFBTSx5QkFBeUIsR0FBRyxJQUFJLENBQUM7QUFFdkM7O0dBRUc7QUFDSCxNQUFNLGdCQUFnQixHQUFHLE1BQU0sQ0FBQyxZQUFZLENBQUMsRUFBRSxDQUFDLENBQUM7QUEyRGpEOztHQUVHO0FBQ0ksTUFBTSxzQkFBc0I7SUFDakM7O09BRUc7SUFDSDtRQWlJUSxjQUFTLEdBQUcsSUFBSSw0Q0FBRyxDQUFDLEVBQUUsV0FBVyxFQUFFLElBQUksRUFBRSxDQUFDLENBQUM7UUFDM0MsZUFBVSxHQUFHLElBQUksNENBQUcsRUFBRSxDQUFDO1FBakk3QixJQUFJLENBQUMsU0FBUyxDQUFDLFNBQVMsQ0FBQyxnREFBTSxFQUFFLDBCQUEwQixDQUFDLENBQUM7UUFDN0QsSUFBSSxDQUFDLFVBQVUsQ0FBQyxTQUFTLENBQUMsZ0RBQU0sRUFBRSwwQkFBMEIsQ0FBQyxDQUFDO0lBQ2hFLENB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SSxNQUFNLENBQUMsSUFBSSxNQUFNLENBQUMsSUFBSSxLQUFLLFFBQVEsRUFBRTtZQUN0RCxPQUFPLE1BQU0sQ0FBQyxPQUFPLENBQUM7U0FDdkI7UUFFRCxnREFBZ0Q7UUFDaEQsTUFBTSxNQUFNLEdBQUcsK0RBQWdCLENBQUMsTUFBTSxDQUFDLE9BQTRCLENBQUMsQ0FBQztRQUVyRSxvREFBb0Q7UUFDcEQsTUFBTSxLQUFLLEdBQUcsTUFBTSxDQUFDLFVBQVUsSUFBSSxFQUFFLENBQUM7UUFDdEMsS0FBSyxNQUFNLFFBQVEsSUFBSSxLQUFLLEVBQUU7WUFDNUIsTUFBTSxDQUFDLFFBQVEsQ0FBQyxHQUFHLFlBQVksQ0FBQyxLQUFLLENBQUMsUUFBUSxDQUFDLENBQUMsQ0FBQztTQUNsRDtRQUVELE9BQU8sTUFBTSxDQUFDO0lBQ2hCLENBQUM7SUF0QmUsb0JBQVksZUFzQjNCO0FBQ0gsQ0FBQyxFQWhLUyxPQUFPLEtBQVAsT0FBTyxRQWdLaEI7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ3B5Q0Q7OzsrRUFHK0U7QUFTcEQ7QUFLM0Isb0JBQW9CO0FBQ3BCOztHQUVHO0FBQ0ksTUFBTSxnQkFBZ0IsR0FBRyxJQUFJLG9EQUFLLENBQ3ZDLHdDQUF3QyxDQUN6QyxDQUFDIiwiZmlsZSI6InBhY2thZ2VzX3NldHRpbmdyZWdpc3RyeV9saWJfaW5kZXhfanMuZTkzMGM0MTY4ZWM2NDc1NmZmNzQuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxufCBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbnwgRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbnwtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKi9cbi8qKlxuICogQHBhY2thZ2VEb2N1bWVudGF0aW9uXG4gKiBAbW9kdWxlIHNldHRpbmdyZWdpc3RyeVxuICovXG5cbmV4cG9ydCAqIGZyb20gJy4vc2V0dGluZ3JlZ2lzdHJ5JztcbmV4cG9ydCAqIGZyb20gJy4vdG9rZW5zJztcbiIsIi8vIENvcHlyaWdodCAoYykgSnVweXRlciBEZXZlbG9wbWVudCBUZWFtLlxuLy8gRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cblxuaW1wb3J0IHsgSURhdGFDb25uZWN0b3IgfSBmcm9tICdAanVweXRlcmxhYi9zdGF0ZWRiJztcbmltcG9ydCB7IENvbW1hbmRSZWdpc3RyeSB9IGZyb20gJ0BsdW1pbm8vY29tbWFuZHMnO1xuaW1wb3J0IHtcbiAgSlNPTkV4dCxcbiAgSlNPTk9iamVjdCxcbiAgSlNPTlZhbHVlLFxuICBQYXJ0aWFsSlNPTk9iamVjdCxcbiAgUGFydGlhbEpTT05WYWx1ZSxcbiAgUmVhZG9ubHlKU09OT2JqZWN0LFxuICBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0LFxuICBSZWFkb25seVBhcnRpYWxKU09OVmFsdWVcbn0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgRGlzcG9zYWJsZURlbGVnYXRlLCBJRGlzcG9zYWJsZSB9IGZyb20gJ0BsdW1pbm8vZGlzcG9zYWJsZSc7XG5pbXBvcnQgeyBJU2lnbmFsLCBTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgQWp2IGZyb20gJ2Fqdic7XG5pbXBvcnQgKiBhcyBqc29uNSBmcm9tICdqc29uNSc7XG5pbXBvcnQgU0NIRU1BIGZyb20gJy4vcGx1Z2luLXNjaGVtYS5qc29uJztcbmltcG9ydCB7IElTZXR0aW5nUmVnaXN0cnkgfSBmcm9tICcuL3Rva2Vucyc7XG5cbi8qKlxuICogQW4gYWxpYXMgZm9yIHRoZSBKU09OIGRlZXAgY29weSBmdW5jdGlvbi5cbiAqL1xuY29uc3QgY29weSA9IEpTT05FeHQuZGVlcENvcHk7XG5cbi8qKlxuICogVGhlIGRlZmF1bHQgbnVtYmVyIG9mIG1pbGxpc2Vjb25kcyBiZWZvcmUgYSBgbG9hZCgpYCBjYWxsIHRvIHRoZSByZWdpc3RyeVxuICogd2lsbCB3YWl0IGJlZm9yZSB0aW1pbmcgb3V0IGlmIGl0IHJlcXVpcmVzIGEgdHJhbnNmb3JtYXRpb24gdGhhdCBoYXMgbm90IGJlZW5cbiAqIHJlZ2lzdGVyZWQuXG4gKi9cbmNvbnN0IERFRkFVTFRfVFJBTlNGT1JNX1RJTUVPVVQgPSAxMDAwO1xuXG4vKipcbiAqIFRoZSBBU0NJSSByZWNvcmQgc2VwYXJhdG9yIGNoYXJhY3Rlci5cbiAqL1xuY29uc3QgUkVDT1JEX1NFUEFSQVRPUiA9IFN0cmluZy5mcm9tQ2hhckNvZGUoMzApO1xuXG4vKipcbiAqIEFuIGltcGxlbWVudGF0aW9uIG9mIGEgc2NoZW1hIHZhbGlkYXRvci5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJU2NoZW1hVmFsaWRhdG9yIHtcbiAgLyoqXG4gICAqIFZhbGlkYXRlIGEgcGx1Z2luJ3Mgc2NoZW1hIGFuZCB1c2VyIGRhdGE7IHBvcHVsYXRlIHRoZSBgY29tcG9zaXRlYCBkYXRhLlxuICAgKlxuICAgKiBAcGFyYW0gcGx1Z2luIC0gVGhlIHBsdWdpbiBiZWluZyB2YWxpZGF0ZWQuIEl0cyBgY29tcG9zaXRlYCBkYXRhIHdpbGwgYmVcbiAgICogcG9wdWxhdGVkIGJ5IHJlZmVyZW5jZS5cbiAgICpcbiAgICogQHBhcmFtIHBvcHVsYXRlIC0gV2hldGhlciBwbHVnaW4gZGF0YSBzaG91bGQgYmUgcG9wdWxhdGVkLCBkZWZhdWx0cyB0b1xuICAgKiBgdHJ1ZWAuXG4gICAqXG4gICAqIEByZXR1cm4gQSBsaXN0IG9mIGVycm9ycyBpZiBlaXRoZXIgdGhlIHNjaGVtYSBvciBkYXRhIGZhaWwgdG8gdmFsaWRhdGUgb3JcbiAgICogYG51bGxgIGlmIHRoZXJlIGFyZSBubyBlcnJvcnMuXG4gICAqL1xuICB2YWxpZGF0ZURhdGEoXG4gICAgcGx1Z2luOiBJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW4sXG4gICAgcG9wdWxhdGU/OiBib29sZWFuXG4gICk6IElTY2hlbWFWYWxpZGF0b3IuSUVycm9yW10gfCBudWxsO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBzY2hlbWEgdmFsaWRhdG9yIGludGVyZmFjZXMuXG4gKi9cbmV4cG9ydCBuYW1lc3BhY2UgSVNjaGVtYVZhbGlkYXRvciB7XG4gIC8qKlxuICAgKiBBIHNjaGVtYSB2YWxpZGF0aW9uIGVycm9yIGRlZmluaXRpb24uXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElFcnJvciB7XG4gICAgLyoqXG4gICAgICogVGhlIHBhdGggaW4gdGhlIGRhdGEgd2hlcmUgdGhlIGVycm9yIG9jY3VycmVkLlxuICAgICAqL1xuICAgIGRhdGFQYXRoOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUga2V5d29yZCB3aG9zZSB2YWxpZGF0aW9uIGZhaWxlZC5cbiAgICAgKi9cbiAgICBrZXl3b3JkOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgZXJyb3IgbWVzc2FnZS5cbiAgICAgKi9cbiAgICBtZXNzYWdlOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBPcHRpb25hbCBwYXJhbWV0ZXIgbWV0YWRhdGEgdGhhdCBtaWdodCBiZSBpbmNsdWRlZCBpbiBhbiBlcnJvci5cbiAgICAgKi9cbiAgICBwYXJhbXM/OiBSZWFkb25seUpTT05PYmplY3Q7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgcGF0aCBpbiB0aGUgc2NoZW1hIHdoZXJlIHRoZSBlcnJvciBvY2N1cnJlZC5cbiAgICAgKi9cbiAgICBzY2hlbWFQYXRoOiBzdHJpbmc7XG4gIH1cbn1cblxuLyoqXG4gKiBUaGUgZGVmYXVsdCBpbXBsZW1lbnRhdGlvbiBvZiBhIHNjaGVtYSB2YWxpZGF0b3IuXG4gKi9cbmV4cG9ydCBjbGFzcyBEZWZhdWx0U2NoZW1hVmFsaWRhdG9yIGltcGxlbWVudHMgSVNjaGVtYVZhbGlkYXRvciB7XG4gIC8qKlxuICAgKiBJbnN0YW50aWF0ZSBhIHNjaGVtYSB2YWxpZGF0b3IuXG4gICAqL1xuICBjb25zdHJ1Y3RvcigpIHtcbiAgICB0aGlzLl9jb21wb3Nlci5hZGRTY2hlbWEoU0NIRU1BLCAnanVweXRlcmxhYi1wbHVnaW4tc2NoZW1hJyk7XG4gICAgdGhpcy5fdmFsaWRhdG9yLmFkZFNjaGVtYShTQ0hFTUEsICdqdXB5dGVybGFiLXBsdWdpbi1zY2hlbWEnKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBWYWxpZGF0ZSBhIHBsdWdpbidzIHNjaGVtYSBhbmQgdXNlciBkYXRhOyBwb3B1bGF0ZSB0aGUgYGNvbXBvc2l0ZWAgZGF0YS5cbiAgICpcbiAgICogQHBhcmFtIHBsdWdpbiAtIFRoZSBwbHVnaW4gYmVpbmcgdmFsaWRhdGVkLiBJdHMgYGNvbXBvc2l0ZWAgZGF0YSB3aWxsIGJlXG4gICAqIHBvcHVsYXRlZCBieSByZWZlcmVuY2UuXG4gICAqXG4gICAqIEBwYXJhbSBwb3B1bGF0ZSAtIFdoZXRoZXIgcGx1Z2luIGRhdGEgc2hvdWxkIGJlIHBvcHVsYXRlZCwgZGVmYXVsdHMgdG9cbiAgICogYHRydWVgLlxuICAgKlxuICAgKiBAcmV0dXJuIEEgbGlzdCBvZiBlcnJvcnMgaWYgZWl0aGVyIHRoZSBzY2hlbWEgb3IgZGF0YSBmYWlsIHRvIHZhbGlkYXRlIG9yXG4gICAqIGBudWxsYCBpZiB0aGVyZSBhcmUgbm8gZXJyb3JzLlxuICAgKi9cbiAgdmFsaWRhdGVEYXRhKFxuICAgIHBsdWdpbjogSVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luLFxuICAgIHBvcHVsYXRlID0gdHJ1ZVxuICApOiBJU2NoZW1hVmFsaWRhdG9yLklFcnJvcltdIHwgbnVsbCB7XG4gICAgY29uc3QgdmFsaWRhdGUgPSB0aGlzLl92YWxpZGF0b3IuZ2V0U2NoZW1hKHBsdWdpbi5pZCk7XG4gICAgY29uc3QgY29tcG9zZSA9IHRoaXMuX2NvbXBvc2VyLmdldFNjaGVtYShwbHVnaW4uaWQpO1xuXG4gICAgLy8gSWYgdGhlIHNjaGVtYXMgZG8gbm90IGV4aXN0LCBhZGQgdGhlbSB0byB0aGUgdmFsaWRhdG9yIGFuZCBjb250aW51ZS5cbiAgICBpZiAoIXZhbGlkYXRlIHx8ICFjb21wb3NlKSB7XG4gICAgICBpZiAocGx1Z2luLnNjaGVtYS50eXBlICE9PSAnb2JqZWN0Jykge1xuICAgICAgICBjb25zdCBrZXl3b3JkID0gJ3NjaGVtYSc7XG4gICAgICAgIGNvbnN0IG1lc3NhZ2UgPVxuICAgICAgICAgIGBTZXR0aW5nIHJlZ2lzdHJ5IHNjaGVtYXMnIHJvb3QtbGV2ZWwgdHlwZSBtdXN0IGJlIGAgK1xuICAgICAgICAgIGAnb2JqZWN0JywgcmVqZWN0aW5nIHR5cGU6ICR7cGx1Z2luLnNjaGVtYS50eXBlfWA7XG5cbiAgICAgICAgcmV0dXJuIFt7IGRhdGFQYXRoOiAndHlwZScsIGtleXdvcmQsIHNjaGVtYVBhdGg6ICcnLCBtZXNzYWdlIH1dO1xuICAgICAgfVxuXG4gICAgICBjb25zdCBlcnJvcnMgPSB0aGlzLl9hZGRTY2hlbWEocGx1Z2luLmlkLCBwbHVnaW4uc2NoZW1hKTtcblxuICAgICAgcmV0dXJuIGVycm9ycyB8fCB0aGlzLnZhbGlkYXRlRGF0YShwbHVnaW4pO1xuICAgIH1cblxuICAgIC8vIFBhcnNlIHRoZSByYXcgY29tbWVudGVkIEpTT04gaW50byBhIHVzZXIgbWFwLlxuICAgIGxldCB1c2VyOiBKU09OT2JqZWN0O1xuICAgIHRyeSB7XG4gICAgICB1c2VyID0ganNvbjUucGFyc2UocGx1Z2luLnJhdykgYXMgSlNPTk9iamVjdDtcbiAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgaWYgKGVycm9yIGluc3RhbmNlb2YgU3ludGF4RXJyb3IpIHtcbiAgICAgICAgcmV0dXJuIFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBkYXRhUGF0aDogJycsXG4gICAgICAgICAgICBrZXl3b3JkOiAnc3ludGF4JyxcbiAgICAgICAgICAgIHNjaGVtYVBhdGg6ICcnLFxuICAgICAgICAgICAgbWVzc2FnZTogZXJyb3IubWVzc2FnZVxuICAgICAgICAgIH1cbiAgICAgICAgXTtcbiAgICAgIH1cblxuICAgICAgY29uc3QgeyBjb2x1bW4sIGRlc2NyaXB0aW9uIH0gPSBlcnJvcjtcbiAgICAgIGNvbnN0IGxpbmUgPSBlcnJvci5saW5lTnVtYmVyO1xuXG4gICAgICByZXR1cm4gW1xuICAgICAgICB7XG4gICAgICAgICAgZGF0YVBhdGg6ICcnLFxuICAgICAgICAgIGtleXdvcmQ6ICdwYXJzZScsXG4gICAgICAgICAgc2NoZW1hUGF0aDogJycsXG4gICAgICAgICAgbWVzc2FnZTogYCR7ZGVzY3JpcHRpb259IChsaW5lICR7bGluZX0gY29sdW1uICR7Y29sdW1ufSlgXG4gICAgICAgIH1cbiAgICAgIF07XG4gICAgfVxuXG4gICAgaWYgKCF2YWxpZGF0ZSh1c2VyKSkge1xuICAgICAgcmV0dXJuIHZhbGlkYXRlLmVycm9ycyBhcyBJU2NoZW1hVmFsaWRhdG9yLklFcnJvcltdO1xuICAgIH1cblxuICAgIC8vIENvcHkgdGhlIHVzZXIgZGF0YSBiZWZvcmUgbWVyZ2luZyBkZWZhdWx0cyBpbnRvIGNvbXBvc2l0ZSBtYXAuXG4gICAgY29uc3QgY29tcG9zaXRlID0gY29weSh1c2VyKTtcblxuICAgIGlmICghY29tcG9zZShjb21wb3NpdGUpKSB7XG4gICAgICByZXR1cm4gY29tcG9zZS5lcnJvcnMgYXMgSVNjaGVtYVZhbGlkYXRvci5JRXJyb3JbXTtcbiAgICB9XG5cbiAgICBpZiAocG9wdWxhdGUpIHtcbiAgICAgIHBsdWdpbi5kYXRhID0geyBjb21wb3NpdGUsIHVzZXIgfTtcbiAgICB9XG5cbiAgICByZXR1cm4gbnVsbDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBZGQgYSBzY2hlbWEgdG8gdGhlIHZhbGlkYXRvci5cbiAgICpcbiAgICogQHBhcmFtIHBsdWdpbiAtIFRoZSBwbHVnaW4gSUQuXG4gICAqXG4gICAqIEBwYXJhbSBzY2hlbWEgLSBUaGUgc2NoZW1hIGJlaW5nIGFkZGVkLlxuICAgKlxuICAgKiBAcmV0dXJuIEEgbGlzdCBvZiBlcnJvcnMgaWYgdGhlIHNjaGVtYSBmYWlscyB0byB2YWxpZGF0ZSBvciBgbnVsbGAgaWYgdGhlcmVcbiAgICogYXJlIG5vIGVycm9ycy5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBJdCBpcyBzYWZlIHRvIGNhbGwgdGhpcyBmdW5jdGlvbiBtdWx0aXBsZSB0aW1lcyB3aXRoIHRoZSBzYW1lIHBsdWdpbiBuYW1lLlxuICAgKi9cbiAgcHJpdmF0ZSBfYWRkU2NoZW1hKFxuICAgIHBsdWdpbjogc3RyaW5nLFxuICAgIHNjaGVtYTogSVNldHRpbmdSZWdpc3RyeS5JU2NoZW1hXG4gICk6IElTY2hlbWFWYWxpZGF0b3IuSUVycm9yW10gfCBudWxsIHtcbiAgICBjb25zdCBjb21wb3NlciA9IHRoaXMuX2NvbXBvc2VyO1xuICAgIGNvbnN0IHZhbGlkYXRvciA9IHRoaXMuX3ZhbGlkYXRvcjtcbiAgICBjb25zdCB2YWxpZGF0ZSA9IHZhbGlkYXRvci5nZXRTY2hlbWEoJ2p1cHl0ZXJsYWItcGx1Z2luLXNjaGVtYScpITtcblxuICAgIC8vIFZhbGlkYXRlIGFnYWluc3QgdGhlIG1haW4gc2NoZW1hLlxuICAgIGlmICghKHZhbGlkYXRlIShzY2hlbWEpIGFzIGJvb2xlYW4pKSB7XG4gICAgICByZXR1cm4gdmFsaWRhdGUhLmVycm9ycyBhcyBJU2NoZW1hVmFsaWRhdG9yLklFcnJvcltdO1xuICAgIH1cblxuICAgIC8vIFZhbGlkYXRlIGFnYWluc3QgdGhlIEpTT04gc2NoZW1hIG1ldGEtc2NoZW1hLlxuICAgIGlmICghKHZhbGlkYXRvci52YWxpZGF0ZVNjaGVtYShzY2hlbWEpIGFzIGJvb2xlYW4pKSB7XG4gICAgICByZXR1cm4gdmFsaWRhdG9yLmVycm9ycyBhcyBJU2NoZW1hVmFsaWRhdG9yLklFcnJvcltdO1xuICAgIH1cblxuICAgIC8vIFJlbW92ZSBpZiBzY2hlbWEgYWxyZWFkeSBleGlzdHMuXG4gICAgY29tcG9zZXIucmVtb3ZlU2NoZW1hKHBsdWdpbik7XG4gICAgdmFsaWRhdG9yLnJlbW92ZVNjaGVtYShwbHVnaW4pO1xuXG4gICAgLy8gQWRkIHNjaGVtYSB0byB0aGUgdmFsaWRhdG9yIGFuZCBjb21wb3Nlci5cbiAgICBjb21wb3Nlci5hZGRTY2hlbWEoc2NoZW1hLCBwbHVnaW4pO1xuICAgIHZhbGlkYXRvci5hZGRTY2hlbWEoc2NoZW1hLCBwbHVnaW4pO1xuXG4gICAgcmV0dXJuIG51bGw7XG4gIH1cblxuICBwcml2YXRlIF9jb21wb3NlciA9IG5ldyBBanYoeyB1c2VEZWZhdWx0czogdHJ1ZSB9KTtcbiAgcHJpdmF0ZSBfdmFsaWRhdG9yID0gbmV3IEFqdigpO1xufVxuXG4vKipcbiAqIFRoZSBkZWZhdWx0IGNvbmNyZXRlIGltcGxlbWVudGF0aW9uIG9mIGEgc2V0dGluZyByZWdpc3RyeS5cbiAqL1xuZXhwb3J0IGNsYXNzIFNldHRpbmdSZWdpc3RyeSBpbXBsZW1lbnRzIElTZXR0aW5nUmVnaXN0cnkge1xuICAvKipcbiAgICogQ3JlYXRlIGEgbmV3IHNldHRpbmcgcmVnaXN0cnkuXG4gICAqL1xuICBjb25zdHJ1Y3RvcihvcHRpb25zOiBTZXR0aW5nUmVnaXN0cnkuSU9wdGlvbnMpIHtcbiAgICB0aGlzLmNvbm5lY3RvciA9IG9wdGlvbnMuY29ubmVjdG9yO1xuICAgIHRoaXMudmFsaWRhdG9yID0gb3B0aW9ucy52YWxpZGF0b3IgfHwgbmV3IERlZmF1bHRTY2hlbWFWYWxpZGF0b3IoKTtcbiAgICB0aGlzLl90aW1lb3V0ID0gb3B0aW9ucy50aW1lb3V0IHx8IERFRkFVTFRfVFJBTlNGT1JNX1RJTUVPVVQ7XG5cbiAgICAvLyBQcmVsb2FkIHdpdGggYW55IGF2YWlsYWJsZSBkYXRhIGF0IGluc3RhbnRpYXRpb24tdGltZS5cbiAgICBpZiAob3B0aW9ucy5wbHVnaW5zKSB7XG4gICAgICB0aGlzLl9yZWFkeSA9IHRoaXMuX3ByZWxvYWQob3B0aW9ucy5wbHVnaW5zKTtcbiAgICB9XG4gIH1cblxuICAvKipcbiAgICogVGhlIGRhdGEgY29ubmVjdG9yIHVzZWQgYnkgdGhlIHNldHRpbmcgcmVnaXN0cnkuXG4gICAqL1xuICByZWFkb25seSBjb25uZWN0b3I6IElEYXRhQ29ubmVjdG9yPElTZXR0aW5nUmVnaXN0cnkuSVBsdWdpbiwgc3RyaW5nLCBzdHJpbmc+O1xuXG4gIC8qKlxuICAgKiBUaGUgc2NoZW1hIG9mIHRoZSBzZXR0aW5nIHJlZ2lzdHJ5LlxuICAgKi9cbiAgcmVhZG9ubHkgc2NoZW1hID0gU0NIRU1BIGFzIElTZXR0aW5nUmVnaXN0cnkuSVNjaGVtYTtcblxuICAvKipcbiAgICogVGhlIHNjaGVtYSB2YWxpZGF0b3IgdXNlZCBieSB0aGUgc2V0dGluZyByZWdpc3RyeS5cbiAgICovXG4gIHJlYWRvbmx5IHZhbGlkYXRvcjogSVNjaGVtYVZhbGlkYXRvcjtcblxuICAvKipcbiAgICogQSBzaWduYWwgdGhhdCBlbWl0cyB0aGUgbmFtZSBvZiBhIHBsdWdpbiB3aGVuIGl0cyBzZXR0aW5ncyBjaGFuZ2UuXG4gICAqL1xuICBnZXQgcGx1Z2luQ2hhbmdlZCgpOiBJU2lnbmFsPHRoaXMsIHN0cmluZz4ge1xuICAgIHJldHVybiB0aGlzLl9wbHVnaW5DaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjb2xsZWN0aW9uIG9mIHNldHRpbmcgcmVnaXN0cnkgcGx1Z2lucy5cbiAgICovXG4gIHJlYWRvbmx5IHBsdWdpbnM6IHtcbiAgICBbbmFtZTogc3RyaW5nXTogSVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luO1xuICB9ID0gT2JqZWN0LmNyZWF0ZShudWxsKTtcblxuICAvKipcbiAgICogR2V0IGFuIGluZGl2aWR1YWwgc2V0dGluZy5cbiAgICpcbiAgICogQHBhcmFtIHBsdWdpbiAtIFRoZSBuYW1lIG9mIHRoZSBwbHVnaW4gd2hvc2Ugc2V0dGluZ3MgYXJlIGJlaW5nIHJldHJpZXZlZC5cbiAgICpcbiAgICogQHBhcmFtIGtleSAtIFRoZSBuYW1lIG9mIHRoZSBzZXR0aW5nIGJlaW5nIHJldHJpZXZlZC5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2hlbiB0aGUgc2V0dGluZyBpcyByZXRyaWV2ZWQuXG4gICAqL1xuICBhc3luYyBnZXQoXG4gICAgcGx1Z2luOiBzdHJpbmcsXG4gICAga2V5OiBzdHJpbmdcbiAgKTogUHJvbWlzZTx7XG4gICAgY29tcG9zaXRlOiBQYXJ0aWFsSlNPTlZhbHVlIHwgdW5kZWZpbmVkO1xuICAgIHVzZXI6IFBhcnRpYWxKU09OVmFsdWUgfCB1bmRlZmluZWQ7XG4gIH0+IHtcbiAgICAvLyBXYWl0IGZvciBkYXRhIHByZWxvYWQgYmVmb3JlIGFsbG93aW5nIG5vcm1hbCBvcGVyYXRpb24uXG4gICAgYXdhaXQgdGhpcy5fcmVhZHk7XG5cbiAgICBjb25zdCBwbHVnaW5zID0gdGhpcy5wbHVnaW5zO1xuXG4gICAgaWYgKHBsdWdpbiBpbiBwbHVnaW5zKSB7XG4gICAgICBjb25zdCB7IGNvbXBvc2l0ZSwgdXNlciB9ID0gcGx1Z2luc1twbHVnaW5dLmRhdGE7XG5cbiAgICAgIHJldHVybiB7XG4gICAgICAgIGNvbXBvc2l0ZTpcbiAgICAgICAgICBjb21wb3NpdGVba2V5XSAhPT0gdW5kZWZpbmVkID8gY29weShjb21wb3NpdGVba2V5XSEpIDogdW5kZWZpbmVkLFxuICAgICAgICB1c2VyOiB1c2VyW2tleV0gIT09IHVuZGVmaW5lZCA/IGNvcHkodXNlcltrZXldISkgOiB1bmRlZmluZWRcbiAgICAgIH07XG4gICAgfVxuXG4gICAgcmV0dXJuIHRoaXMubG9hZChwbHVnaW4pLnRoZW4oKCkgPT4gdGhpcy5nZXQocGx1Z2luLCBrZXkpKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBMb2FkIGEgcGx1Z2luJ3Mgc2V0dGluZ3MgaW50byB0aGUgc2V0dGluZyByZWdpc3RyeS5cbiAgICpcbiAgICogQHBhcmFtIHBsdWdpbiAtIFRoZSBuYW1lIG9mIHRoZSBwbHVnaW4gd2hvc2Ugc2V0dGluZ3MgYXJlIGJlaW5nIGxvYWRlZC5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2l0aCBhIHBsdWdpbiBzZXR0aW5ncyBvYmplY3Qgb3IgcmVqZWN0c1xuICAgKiBpZiB0aGUgcGx1Z2luIGlzIG5vdCBmb3VuZC5cbiAgICovXG4gIGFzeW5jIGxvYWQocGx1Z2luOiBzdHJpbmcpOiBQcm9taXNlPElTZXR0aW5nUmVnaXN0cnkuSVNldHRpbmdzPiB7XG4gICAgLy8gV2FpdCBmb3IgZGF0YSBwcmVsb2FkIGJlZm9yZSBhbGxvd2luZyBub3JtYWwgb3BlcmF0aW9uLlxuICAgIGF3YWl0IHRoaXMuX3JlYWR5O1xuXG4gICAgY29uc3QgcGx1Z2lucyA9IHRoaXMucGx1Z2lucztcbiAgICBjb25zdCByZWdpc3RyeSA9IHRoaXM7IC8vIGVzbGludC1kaXNhYmxlLWxpbmVcblxuICAgIC8vIElmIHRoZSBwbHVnaW4gZXhpc3RzLCByZXNvbHZlLlxuICAgIGlmIChwbHVnaW4gaW4gcGx1Z2lucykge1xuICAgICAgcmV0dXJuIG5ldyBTZXR0aW5ncyh7IHBsdWdpbjogcGx1Z2luc1twbHVnaW5dLCByZWdpc3RyeSB9KTtcbiAgICB9XG5cbiAgICAvLyBJZiB0aGUgcGx1Z2luIG5lZWRzIHRvIGJlIGxvYWRlZCBmcm9tIHRoZSBkYXRhIGNvbm5lY3RvciwgZmV0Y2guXG4gICAgcmV0dXJuIHRoaXMucmVsb2FkKHBsdWdpbik7XG4gIH1cblxuICAvKipcbiAgICogUmVsb2FkIGEgcGx1Z2luJ3Mgc2V0dGluZ3MgaW50byB0aGUgcmVnaXN0cnkgZXZlbiBpZiB0aGV5IGFscmVhZHkgZXhpc3QuXG4gICAqXG4gICAqIEBwYXJhbSBwbHVnaW4gLSBUaGUgbmFtZSBvZiB0aGUgcGx1Z2luIHdob3NlIHNldHRpbmdzIGFyZSBiZWluZyByZWxvYWRlZC5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2l0aCBhIHBsdWdpbiBzZXR0aW5ncyBvYmplY3Qgb3IgcmVqZWN0c1xuICAgKiB3aXRoIGEgbGlzdCBvZiBgSVNjaGVtYVZhbGlkYXRvci5JRXJyb3JgIG9iamVjdHMgaWYgaXQgZmFpbHMuXG4gICAqL1xuICBhc3luYyByZWxvYWQocGx1Z2luOiBzdHJpbmcpOiBQcm9taXNlPElTZXR0aW5nUmVnaXN0cnkuSVNldHRpbmdzPiB7XG4gICAgLy8gV2FpdCBmb3IgZGF0YSBwcmVsb2FkIGJlZm9yZSBhbGxvd2luZyBub3JtYWwgb3BlcmF0aW9uLlxuICAgIGF3YWl0IHRoaXMuX3JlYWR5O1xuXG4gICAgY29uc3QgZmV0Y2hlZCA9IGF3YWl0IHRoaXMuY29ubmVjdG9yLmZldGNoKHBsdWdpbik7XG4gICAgY29uc3QgcGx1Z2lucyA9IHRoaXMucGx1Z2luczsgLy8gZXNsaW50LWRpc2FibGUtbGluZVxuICAgIGNvbnN0IHJlZ2lzdHJ5ID0gdGhpczsgLy8gZXNsaW50LWRpc2FibGUtbGluZVxuXG4gICAgaWYgKGZldGNoZWQgPT09IHVuZGVmaW5lZCkge1xuICAgICAgdGhyb3cgW1xuICAgICAgICB7XG4gICAgICAgICAgZGF0YVBhdGg6ICcnLFxuICAgICAgICAgIGtleXdvcmQ6ICdpZCcsXG4gICAgICAgICAgbWVzc2FnZTogYENvdWxkIG5vdCBmZXRjaCBzZXR0aW5ncyBmb3IgJHtwbHVnaW59LmAsXG4gICAgICAgICAgc2NoZW1hUGF0aDogJydcbiAgICAgICAgfSBhcyBJU2NoZW1hVmFsaWRhdG9yLklFcnJvclxuICAgICAgXTtcbiAgICB9XG4gICAgYXdhaXQgdGhpcy5fbG9hZChhd2FpdCB0aGlzLl90cmFuc2Zvcm0oJ2ZldGNoJywgZmV0Y2hlZCkpO1xuICAgIHRoaXMuX3BsdWdpbkNoYW5nZWQuZW1pdChwbHVnaW4pO1xuXG4gICAgcmV0dXJuIG5ldyBTZXR0aW5ncyh7IHBsdWdpbjogcGx1Z2luc1twbHVnaW5dLCByZWdpc3RyeSB9KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW1vdmUgYSBzaW5nbGUgc2V0dGluZyBpbiB0aGUgcmVnaXN0cnkuXG4gICAqXG4gICAqIEBwYXJhbSBwbHVnaW4gLSBUaGUgbmFtZSBvZiB0aGUgcGx1Z2luIHdob3NlIHNldHRpbmcgaXMgYmVpbmcgcmVtb3ZlZC5cbiAgICpcbiAgICogQHBhcmFtIGtleSAtIFRoZSBuYW1lIG9mIHRoZSBzZXR0aW5nIGJlaW5nIHJlbW92ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIHNldHRpbmcgaXMgcmVtb3ZlZC5cbiAgICovXG4gIGFzeW5jIHJlbW92ZShwbHVnaW46IHN0cmluZywga2V5OiBzdHJpbmcpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICAvLyBXYWl0IGZvciBkYXRhIHByZWxvYWQgYmVmb3JlIGFsbG93aW5nIG5vcm1hbCBvcGVyYXRpb24uXG4gICAgYXdhaXQgdGhpcy5fcmVhZHk7XG5cbiAgICBjb25zdCBwbHVnaW5zID0gdGhpcy5wbHVnaW5zO1xuXG4gICAgaWYgKCEocGx1Z2luIGluIHBsdWdpbnMpKSB7XG4gICAgICByZXR1cm47XG4gICAgfVxuXG4gICAgY29uc3QgcmF3ID0ganNvbjUucGFyc2UocGx1Z2luc1twbHVnaW5dLnJhdyk7XG5cbiAgICAvLyBEZWxldGUgYm90aCB0aGUgdmFsdWUgYW5kIGFueSBhc3NvY2lhdGVkIGNvbW1lbnQuXG4gICAgZGVsZXRlIHJhd1trZXldO1xuICAgIGRlbGV0ZSByYXdbYC8vICR7a2V5fWBdO1xuICAgIHBsdWdpbnNbcGx1Z2luXS5yYXcgPSBQcml2YXRlLmFubm90YXRlZFBsdWdpbihwbHVnaW5zW3BsdWdpbl0sIHJhdyk7XG5cbiAgICByZXR1cm4gdGhpcy5fc2F2ZShwbHVnaW4pO1xuICB9XG5cbiAgLyoqXG4gICAqIFNldCBhIHNpbmdsZSBzZXR0aW5nIGluIHRoZSByZWdpc3RyeS5cbiAgICpcbiAgICogQHBhcmFtIHBsdWdpbiAtIFRoZSBuYW1lIG9mIHRoZSBwbHVnaW4gd2hvc2Ugc2V0dGluZyBpcyBiZWluZyBzZXQuXG4gICAqXG4gICAqIEBwYXJhbSBrZXkgLSBUaGUgbmFtZSBvZiB0aGUgc2V0dGluZyBiZWluZyBzZXQuXG4gICAqXG4gICAqIEBwYXJhbSB2YWx1ZSAtIFRoZSB2YWx1ZSBvZiB0aGUgc2V0dGluZyBiZWluZyBzZXQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIHNldHRpbmcgaGFzIGJlZW4gc2F2ZWQuXG4gICAqXG4gICAqL1xuICBhc3luYyBzZXQocGx1Z2luOiBzdHJpbmcsIGtleTogc3RyaW5nLCB2YWx1ZTogSlNPTlZhbHVlKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgLy8gV2FpdCBmb3IgZGF0YSBwcmVsb2FkIGJlZm9yZSBhbGxvd2luZyBub3JtYWwgb3BlcmF0aW9uLlxuICAgIGF3YWl0IHRoaXMuX3JlYWR5O1xuXG4gICAgY29uc3QgcGx1Z2lucyA9IHRoaXMucGx1Z2lucztcblxuICAgIGlmICghKHBsdWdpbiBpbiBwbHVnaW5zKSkge1xuICAgICAgcmV0dXJuIHRoaXMubG9hZChwbHVnaW4pLnRoZW4oKCkgPT4gdGhpcy5zZXQocGx1Z2luLCBrZXksIHZhbHVlKSk7XG4gICAgfVxuXG4gICAgLy8gUGFyc2UgdGhlIHJhdyBKU09OIHN0cmluZyByZW1vdmluZyBhbGwgY29tbWVudHMgYW5kIHJldHVybiBhbiBvYmplY3QuXG4gICAgY29uc3QgcmF3ID0ganNvbjUucGFyc2UocGx1Z2luc1twbHVnaW5dLnJhdyk7XG5cbiAgICBwbHVnaW5zW3BsdWdpbl0ucmF3ID0gUHJpdmF0ZS5hbm5vdGF0ZWRQbHVnaW4ocGx1Z2luc1twbHVnaW5dLCB7XG4gICAgICAuLi5yYXcsXG4gICAgICBba2V5XTogdmFsdWVcbiAgICB9KTtcblxuICAgIHJldHVybiB0aGlzLl9zYXZlKHBsdWdpbik7XG4gIH1cblxuICAvKipcbiAgICogUmVnaXN0ZXIgYSBwbHVnaW4gdHJhbnNmb3JtIGZ1bmN0aW9uIHRvIGFjdCBvbiBhIHNwZWNpZmljIHBsdWdpbi5cbiAgICpcbiAgICogQHBhcmFtIHBsdWdpbiAtIFRoZSBuYW1lIG9mIHRoZSBwbHVnaW4gd2hvc2Ugc2V0dGluZ3MgYXJlIHRyYW5zZm9ybWVkLlxuICAgKlxuICAgKiBAcGFyYW0gdHJhbnNmb3JtcyAtIFRoZSB0cmFuc2Zvcm0gZnVuY3Rpb25zIGFwcGxpZWQgdG8gdGhlIHBsdWdpbi5cbiAgICpcbiAgICogQHJldHVybnMgQSBkaXNwb3NhYmxlIHRoYXQgcmVtb3ZlcyB0aGUgdHJhbnNmb3JtcyBmcm9tIHRoZSByZWdpc3RyeS5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiAtIGBjb21wb3NlYCB0cmFuc2Zvcm1hdGlvbnM6IFRoZSByZWdpc3RyeSBhdXRvbWF0aWNhbGx5IG92ZXJ3cml0ZXMgYVxuICAgKiBwbHVnaW4ncyBkZWZhdWx0IHZhbHVlcyB3aXRoIHVzZXIgb3ZlcnJpZGVzLCBidXQgYSBwbHVnaW4gbWF5IGluc3RlYWQgd2lzaFxuICAgKiB0byBtZXJnZSB2YWx1ZXMuIFRoaXMgYmVoYXZpb3IgY2FuIGJlIGFjY29tcGxpc2hlZCBpbiBhIGBjb21wb3NlYFxuICAgKiB0cmFuc2Zvcm1hdGlvbi5cbiAgICogLSBgZmV0Y2hgIHRyYW5zZm9ybWF0aW9uczogVGhlIHJlZ2lzdHJ5IHVzZXMgdGhlIHBsdWdpbiBkYXRhIHRoYXQgaXNcbiAgICogZmV0Y2hlZCBmcm9tIGl0cyBjb25uZWN0b3IuIElmIGEgcGx1Z2luIHdhbnRzIHRvIG92ZXJyaWRlLCBlLmcuIHRvIHVwZGF0ZVxuICAgKiBpdHMgc2NoZW1hIHdpdGggZHluYW1pYyBkZWZhdWx0cywgYSBgZmV0Y2hgIHRyYW5zZm9ybWF0aW9uIGNhbiBiZSBhcHBsaWVkLlxuICAgKi9cbiAgdHJhbnNmb3JtKFxuICAgIHBsdWdpbjogc3RyaW5nLFxuICAgIHRyYW5zZm9ybXM6IHtcbiAgICAgIFtwaGFzZSBpbiBJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW4uUGhhc2VdPzogSVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luLlRyYW5zZm9ybTtcbiAgICB9XG4gICk6IElEaXNwb3NhYmxlIHtcbiAgICBjb25zdCB0cmFuc2Zvcm1lcnMgPSB0aGlzLl90cmFuc2Zvcm1lcnM7XG5cbiAgICBpZiAocGx1Z2luIGluIHRyYW5zZm9ybWVycykge1xuICAgICAgdGhyb3cgbmV3IEVycm9yKGAke3BsdWdpbn0gYWxyZWFkeSBoYXMgYSB0cmFuc2Zvcm1lci5gKTtcbiAgICB9XG5cbiAgICB0cmFuc2Zvcm1lcnNbcGx1Z2luXSA9IHtcbiAgICAgIGZldGNoOiB0cmFuc2Zvcm1zLmZldGNoIHx8IChwbHVnaW4gPT4gcGx1Z2luKSxcbiAgICAgIGNvbXBvc2U6IHRyYW5zZm9ybXMuY29tcG9zZSB8fCAocGx1Z2luID0+IHBsdWdpbilcbiAgICB9O1xuXG4gICAgcmV0dXJuIG5ldyBEaXNwb3NhYmxlRGVsZWdhdGUoKCkgPT4ge1xuICAgICAgZGVsZXRlIHRyYW5zZm9ybWVyc1twbHVnaW5dO1xuICAgIH0pO1xuICB9XG5cbiAgLyoqXG4gICAqIFVwbG9hZCBhIHBsdWdpbidzIHNldHRpbmdzLlxuICAgKlxuICAgKiBAcGFyYW0gcGx1Z2luIC0gVGhlIG5hbWUgb2YgdGhlIHBsdWdpbiB3aG9zZSBzZXR0aW5ncyBhcmUgYmVpbmcgc2V0LlxuICAgKlxuICAgKiBAcGFyYW0gcmF3IC0gVGhlIHJhdyBwbHVnaW4gc2V0dGluZ3MgYmVpbmcgdXBsb2FkZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIHNldHRpbmdzIGhhdmUgYmVlbiBzYXZlZC5cbiAgICovXG4gIGFzeW5jIHVwbG9hZChwbHVnaW46IHN0cmluZywgcmF3OiBzdHJpbmcpOiBQcm9taXNlPHZvaWQ+IHtcbiAgICAvLyBXYWl0IGZvciBkYXRhIHByZWxvYWQgYmVmb3JlIGFsbG93aW5nIG5vcm1hbCBvcGVyYXRpb24uXG4gICAgYXdhaXQgdGhpcy5fcmVhZHk7XG5cbiAgICBjb25zdCBwbHVnaW5zID0gdGhpcy5wbHVnaW5zO1xuXG4gICAgaWYgKCEocGx1Z2luIGluIHBsdWdpbnMpKSB7XG4gICAgICByZXR1cm4gdGhpcy5sb2FkKHBsdWdpbikudGhlbigoKSA9PiB0aGlzLnVwbG9hZChwbHVnaW4sIHJhdykpO1xuICAgIH1cblxuICAgIC8vIFNldCB0aGUgbG9jYWwgY29weS5cbiAgICBwbHVnaW5zW3BsdWdpbl0ucmF3ID0gcmF3O1xuXG4gICAgcmV0dXJuIHRoaXMuX3NhdmUocGx1Z2luKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBMb2FkIGEgcGx1Z2luIGludG8gdGhlIHJlZ2lzdHJ5LlxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBfbG9hZChkYXRhOiBJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW4pOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBjb25zdCBwbHVnaW4gPSBkYXRhLmlkO1xuXG4gICAgLy8gVmFsaWRhdGUgYW5kIHByZWxvYWQgdGhlIGl0ZW0uXG4gICAgdHJ5IHtcbiAgICAgIGF3YWl0IHRoaXMuX3ZhbGlkYXRlKGRhdGEpO1xuICAgIH0gY2F0Y2ggKGVycm9ycykge1xuICAgICAgY29uc3Qgb3V0cHV0ID0gW2BWYWxpZGF0aW5nICR7cGx1Z2lufSBmYWlsZWQ6YF07XG5cbiAgICAgIChlcnJvcnMgYXMgSVNjaGVtYVZhbGlkYXRvci5JRXJyb3JbXSkuZm9yRWFjaCgoZXJyb3IsIGluZGV4KSA9PiB7XG4gICAgICAgIGNvbnN0IHsgZGF0YVBhdGgsIHNjaGVtYVBhdGgsIGtleXdvcmQsIG1lc3NhZ2UgfSA9IGVycm9yO1xuXG4gICAgICAgIGlmIChkYXRhUGF0aCB8fCBzY2hlbWFQYXRoKSB7XG4gICAgICAgICAgb3V0cHV0LnB1c2goYCR7aW5kZXh9IC0gc2NoZW1hIEAgJHtzY2hlbWFQYXRofSwgZGF0YSBAICR7ZGF0YVBhdGh9YCk7XG4gICAgICAgIH1cbiAgICAgICAgb3V0cHV0LnB1c2goYHske2tleXdvcmR9fSAke21lc3NhZ2V9YCk7XG4gICAgICB9KTtcbiAgICAgIGNvbnNvbGUud2FybihvdXRwdXQuam9pbignXFxuJykpO1xuXG4gICAgICB0aHJvdyBlcnJvcnM7XG4gICAgfVxuICB9XG5cbiAgLyoqXG4gICAqIFByZWxvYWQgYSBsaXN0IG9mIHBsdWdpbnMgYW5kIGZhaWwgZ3JhY2VmdWxseS5cbiAgICovXG4gIHByaXZhdGUgYXN5bmMgX3ByZWxvYWQocGx1Z2luczogSVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luW10pOiBQcm9taXNlPHZvaWQ+IHtcbiAgICBhd2FpdCBQcm9taXNlLmFsbChcbiAgICAgIHBsdWdpbnMubWFwKGFzeW5jIHBsdWdpbiA9PiB7XG4gICAgICAgIHRyeSB7XG4gICAgICAgICAgLy8gQXBwbHkgYSB0cmFuc2Zvcm1hdGlvbiB0byB0aGUgcGx1Z2luIGlmIG5lY2Vzc2FyeS5cbiAgICAgICAgICBhd2FpdCB0aGlzLl9sb2FkKGF3YWl0IHRoaXMuX3RyYW5zZm9ybSgnZmV0Y2gnLCBwbHVnaW4pKTtcbiAgICAgICAgfSBjYXRjaCAoZXJyb3JzKSB7XG4gICAgICAgICAgLyogSWdub3JlIHByZWxvYWQgdGltZW91dCBlcnJvcnMgc2lsZW50bHkuICovXG4gICAgICAgICAgaWYgKGVycm9yc1swXT8ua2V5d29yZCAhPT0gJ3RpbWVvdXQnKSB7XG4gICAgICAgICAgICBjb25zb2xlLndhcm4oJ0lnbm9yZWQgc2V0dGluZyByZWdpc3RyeSBwcmVsb2FkIGVycm9ycy4nLCBlcnJvcnMpO1xuICAgICAgICAgIH1cbiAgICAgICAgfVxuICAgICAgfSlcbiAgICApO1xuICB9XG5cbiAgLyoqXG4gICAqIFNhdmUgYSBwbHVnaW4gaW4gdGhlIHJlZ2lzdHJ5LlxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBfc2F2ZShwbHVnaW46IHN0cmluZyk6IFByb21pc2U8dm9pZD4ge1xuICAgIGNvbnN0IHBsdWdpbnMgPSB0aGlzLnBsdWdpbnM7XG5cbiAgICBpZiAoIShwbHVnaW4gaW4gcGx1Z2lucykpIHtcbiAgICAgIHRocm93IG5ldyBFcnJvcihgJHtwbHVnaW59IGRvZXMgbm90IGV4aXN0IGluIHNldHRpbmcgcmVnaXN0cnkuYCk7XG4gICAgfVxuXG4gICAgdHJ5IHtcbiAgICAgIGF3YWl0IHRoaXMuX3ZhbGlkYXRlKHBsdWdpbnNbcGx1Z2luXSk7XG4gICAgfSBjYXRjaCAoZXJyb3JzKSB7XG4gICAgICBjb25zb2xlLndhcm4oYCR7cGx1Z2lufSB2YWxpZGF0aW9uIGVycm9yczpgLCBlcnJvcnMpO1xuICAgICAgdGhyb3cgbmV3IEVycm9yKGAke3BsdWdpbn0gZmFpbGVkIHRvIHZhbGlkYXRlOyBjaGVjayBjb25zb2xlLmApO1xuICAgIH1cbiAgICBhd2FpdCB0aGlzLmNvbm5lY3Rvci5zYXZlKHBsdWdpbiwgcGx1Z2luc1twbHVnaW5dLnJhdyk7XG5cbiAgICAvLyBGZXRjaCBhbmQgcmVsb2FkIHRoZSBkYXRhIHRvIGd1YXJhbnRlZSBzZXJ2ZXIgYW5kIGNsaWVudCBhcmUgaW4gc3luYy5cbiAgICBjb25zdCBmZXRjaGVkID0gYXdhaXQgdGhpcy5jb25uZWN0b3IuZmV0Y2gocGx1Z2luKTtcbiAgICBpZiAoZmV0Y2hlZCA9PT0gdW5kZWZpbmVkKSB7XG4gICAgICB0aHJvdyBbXG4gICAgICAgIHtcbiAgICAgICAgICBkYXRhUGF0aDogJycsXG4gICAgICAgICAga2V5d29yZDogJ2lkJyxcbiAgICAgICAgICBtZXNzYWdlOiBgQ291bGQgbm90IGZldGNoIHNldHRpbmdzIGZvciAke3BsdWdpbn0uYCxcbiAgICAgICAgICBzY2hlbWFQYXRoOiAnJ1xuICAgICAgICB9IGFzIElTY2hlbWFWYWxpZGF0b3IuSUVycm9yXG4gICAgICBdO1xuICAgIH1cbiAgICBhd2FpdCB0aGlzLl9sb2FkKGF3YWl0IHRoaXMuX3RyYW5zZm9ybSgnZmV0Y2gnLCBmZXRjaGVkKSk7XG4gICAgdGhpcy5fcGx1Z2luQ2hhbmdlZC5lbWl0KHBsdWdpbik7XG4gIH1cblxuICAvKipcbiAgICogVHJhbnNmb3JtIHRoZSBwbHVnaW4gaWYgbmVjZXNzYXJ5LlxuICAgKi9cbiAgcHJpdmF0ZSBhc3luYyBfdHJhbnNmb3JtKFxuICAgIHBoYXNlOiBJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW4uUGhhc2UsXG4gICAgcGx1Z2luOiBJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW4sXG4gICAgc3RhcnRlZCA9IG5ldyBEYXRlKCkuZ2V0VGltZSgpXG4gICk6IFByb21pc2U8SVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luPiB7XG4gICAgY29uc3QgZWxhcHNlZCA9IG5ldyBEYXRlKCkuZ2V0VGltZSgpIC0gc3RhcnRlZDtcbiAgICBjb25zdCBpZCA9IHBsdWdpbi5pZDtcbiAgICBjb25zdCB0cmFuc2Zvcm1lcnMgPSB0aGlzLl90cmFuc2Zvcm1lcnM7XG4gICAgY29uc3QgdGltZW91dCA9IHRoaXMuX3RpbWVvdXQ7XG5cbiAgICBpZiAoIXBsdWdpbi5zY2hlbWFbJ2p1cHl0ZXIubGFiLnRyYW5zZm9ybSddKSB7XG4gICAgICByZXR1cm4gcGx1Z2luO1xuICAgIH1cblxuICAgIGlmIChpZCBpbiB0cmFuc2Zvcm1lcnMpIHtcbiAgICAgIGNvbnN0IHRyYW5zZm9ybWVkID0gdHJhbnNmb3JtZXJzW2lkXVtwaGFzZV0uY2FsbChudWxsLCBwbHVnaW4pO1xuXG4gICAgICBpZiAodHJhbnNmb3JtZWQuaWQgIT09IGlkKSB7XG4gICAgICAgIHRocm93IFtcbiAgICAgICAgICB7XG4gICAgICAgICAgICBkYXRhUGF0aDogJycsXG4gICAgICAgICAgICBrZXl3b3JkOiAnaWQnLFxuICAgICAgICAgICAgbWVzc2FnZTogJ1BsdWdpbiB0cmFuc2Zvcm1hdGlvbnMgY2Fubm90IGNoYW5nZSBwbHVnaW4gSURzLicsXG4gICAgICAgICAgICBzY2hlbWFQYXRoOiAnJ1xuICAgICAgICAgIH0gYXMgSVNjaGVtYVZhbGlkYXRvci5JRXJyb3JcbiAgICAgICAgXTtcbiAgICAgIH1cblxuICAgICAgcmV0dXJuIHRyYW5zZm9ybWVkO1xuICAgIH1cblxuICAgIC8vIElmIHRoZSB0aW1lb3V0IGhhcyBub3QgYmVlbiBleGNlZWRlZCwgc3RhbGwgYW5kIHRyeSBhZ2FpbiBpbiAyNTBtcy5cbiAgICBpZiAoZWxhcHNlZCA8IHRpbWVvdXQpIHtcbiAgICAgIGF3YWl0IG5ldyBQcm9taXNlPHZvaWQ+KHJlc29sdmUgPT4ge1xuICAgICAgICBzZXRUaW1lb3V0KCgpID0+IHtcbiAgICAgICAgICByZXNvbHZlKCk7XG4gICAgICAgIH0sIDI1MCk7XG4gICAgICB9KTtcbiAgICAgIHJldHVybiB0aGlzLl90cmFuc2Zvcm0ocGhhc2UsIHBsdWdpbiwgc3RhcnRlZCk7XG4gICAgfVxuXG4gICAgdGhyb3cgW1xuICAgICAge1xuICAgICAgICBkYXRhUGF0aDogJycsXG4gICAgICAgIGtleXdvcmQ6ICd0aW1lb3V0JyxcbiAgICAgICAgbWVzc2FnZTogYFRyYW5zZm9ybWluZyAke3BsdWdpbi5pZH0gdGltZWQgb3V0LmAsXG4gICAgICAgIHNjaGVtYVBhdGg6ICcnXG4gICAgICB9IGFzIElTY2hlbWFWYWxpZGF0b3IuSUVycm9yXG4gICAgXTtcbiAgfVxuXG4gIC8qKlxuICAgKiBWYWxpZGF0ZSBhbmQgcHJlbG9hZCBhIHBsdWdpbiwgY29tcG9zZSB0aGUgYGNvbXBvc2l0ZWAgZGF0YS5cbiAgICovXG4gIHByaXZhdGUgYXN5bmMgX3ZhbGlkYXRlKHBsdWdpbjogSVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgLy8gVmFsaWRhdGUgdGhlIHVzZXIgZGF0YSBhbmQgY3JlYXRlIHRoZSBjb21wb3NpdGUgZGF0YS5cbiAgICBjb25zdCBlcnJvcnMgPSB0aGlzLnZhbGlkYXRvci52YWxpZGF0ZURhdGEocGx1Z2luKTtcblxuICAgIGlmIChlcnJvcnMpIHtcbiAgICAgIHRocm93IGVycm9ycztcbiAgICB9XG5cbiAgICAvLyBBcHBseSBhIHRyYW5zZm9ybWF0aW9uIGlmIG5lY2Vzc2FyeSBhbmQgc2V0IHRoZSBsb2NhbCBjb3B5LlxuICAgIHRoaXMucGx1Z2luc1twbHVnaW4uaWRdID0gYXdhaXQgdGhpcy5fdHJhbnNmb3JtKCdjb21wb3NlJywgcGx1Z2luKTtcbiAgfVxuXG4gIHByaXZhdGUgX3BsdWdpbkNoYW5nZWQgPSBuZXcgU2lnbmFsPHRoaXMsIHN0cmluZz4odGhpcyk7XG4gIHByaXZhdGUgX3JlYWR5ID0gUHJvbWlzZS5yZXNvbHZlKCk7XG4gIHByaXZhdGUgX3RpbWVvdXQ6IG51bWJlcjtcbiAgcHJpdmF0ZSBfdHJhbnNmb3JtZXJzOiB7XG4gICAgW3BsdWdpbjogc3RyaW5nXToge1xuICAgICAgW3BoYXNlIGluIElTZXR0aW5nUmVnaXN0cnkuSVBsdWdpbi5QaGFzZV06IElTZXR0aW5nUmVnaXN0cnkuSVBsdWdpbi5UcmFuc2Zvcm07XG4gICAgfTtcbiAgfSA9IE9iamVjdC5jcmVhdGUobnVsbCk7XG59XG5cbi8qKlxuICogQSBtYW5hZ2VyIGZvciBhIHNwZWNpZmljIHBsdWdpbidzIHNldHRpbmdzLlxuICovXG5leHBvcnQgY2xhc3MgU2V0dGluZ3MgaW1wbGVtZW50cyBJU2V0dGluZ1JlZ2lzdHJ5LklTZXR0aW5ncyB7XG4gIC8qKlxuICAgKiBJbnN0YW50aWF0ZSBhIG5ldyBwbHVnaW4gc2V0dGluZ3MgbWFuYWdlci5cbiAgICovXG4gIGNvbnN0cnVjdG9yKG9wdGlvbnM6IFNldHRpbmdzLklPcHRpb25zKSB7XG4gICAgdGhpcy5pZCA9IG9wdGlvbnMucGx1Z2luLmlkO1xuICAgIHRoaXMucmVnaXN0cnkgPSBvcHRpb25zLnJlZ2lzdHJ5O1xuICAgIHRoaXMucmVnaXN0cnkucGx1Z2luQ2hhbmdlZC5jb25uZWN0KHRoaXMuX29uUGx1Z2luQ2hhbmdlZCwgdGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHBsdWdpbiBuYW1lLlxuICAgKi9cbiAgcmVhZG9ubHkgaWQ6IHN0cmluZztcblxuICAvKipcbiAgICogVGhlIHNldHRpbmcgcmVnaXN0cnkgaW5zdGFuY2UgdXNlZCBhcyBhIGJhY2stZW5kIGZvciB0aGVzZSBzZXR0aW5ncy5cbiAgICovXG4gIHJlYWRvbmx5IHJlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5O1xuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCB0aGF0IGVtaXRzIHdoZW4gdGhlIHBsdWdpbidzIHNldHRpbmdzIGhhdmUgY2hhbmdlZC5cbiAgICovXG4gIGdldCBjaGFuZ2VkKCk6IElTaWduYWw8dGhpcywgdm9pZD4ge1xuICAgIHJldHVybiB0aGlzLl9jaGFuZ2VkO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBjb21wb3NpdGUgb2YgdXNlciBzZXR0aW5ncyBhbmQgZXh0ZW5zaW9uIGRlZmF1bHRzLlxuICAgKi9cbiAgZ2V0IGNvbXBvc2l0ZSgpOiBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0IHtcbiAgICByZXR1cm4gdGhpcy5wbHVnaW4uZGF0YS5jb21wb3NpdGU7XG4gIH1cblxuICAvKipcbiAgICogVGVzdCB3aGV0aGVyIHRoZSBwbHVnaW4gc2V0dGluZ3MgbWFuYWdlciBkaXNwb3NlZC5cbiAgICovXG4gIGdldCBpc0Rpc3Bvc2VkKCk6IGJvb2xlYW4ge1xuICAgIHJldHVybiB0aGlzLl9pc0Rpc3Bvc2VkO1xuICB9XG5cbiAgZ2V0IHBsdWdpbigpOiBJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW4ge1xuICAgIHJldHVybiB0aGlzLnJlZ2lzdHJ5LnBsdWdpbnNbdGhpcy5pZF0hO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBwbHVnaW4ncyBzY2hlbWEuXG4gICAqL1xuICBnZXQgc2NoZW1hKCk6IElTZXR0aW5nUmVnaXN0cnkuSVNjaGVtYSB7XG4gICAgcmV0dXJuIHRoaXMucGx1Z2luLnNjaGVtYTtcbiAgfVxuXG4gIC8qKlxuICAgKiBUaGUgcGx1Z2luIHNldHRpbmdzIHJhdyB0ZXh0IHZhbHVlLlxuICAgKi9cbiAgZ2V0IHJhdygpOiBzdHJpbmcge1xuICAgIHJldHVybiB0aGlzLnBsdWdpbi5yYXc7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHVzZXIgc2V0dGluZ3MuXG4gICAqL1xuICBnZXQgdXNlcigpOiBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0IHtcbiAgICByZXR1cm4gdGhpcy5wbHVnaW4uZGF0YS51c2VyO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBwdWJsaXNoZWQgdmVyc2lvbiBvZiB0aGUgTlBNIHBhY2thZ2UgY29udGFpbmluZyB0aGVzZSBzZXR0aW5ncy5cbiAgICovXG4gIGdldCB2ZXJzaW9uKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIHRoaXMucGx1Z2luLnZlcnNpb247XG4gIH1cblxuICAvKipcbiAgICogUmV0dXJuIHRoZSBkZWZhdWx0cyBpbiBhIGNvbW1lbnRlZCBKU09OIGZvcm1hdC5cbiAgICovXG4gIGFubm90YXRlZERlZmF1bHRzKCk6IHN0cmluZyB7XG4gICAgcmV0dXJuIFByaXZhdGUuYW5ub3RhdGVkRGVmYXVsdHModGhpcy5zY2hlbWEsIHRoaXMuaWQpO1xuICB9XG5cbiAgLyoqXG4gICAqIENhbGN1bGF0ZSB0aGUgZGVmYXVsdCB2YWx1ZSBvZiBhIHNldHRpbmcgYnkgaXRlcmF0aW5nIHRocm91Z2ggdGhlIHNjaGVtYS5cbiAgICpcbiAgICogQHBhcmFtIGtleSAtIFRoZSBuYW1lIG9mIHRoZSBzZXR0aW5nIHdob3NlIGRlZmF1bHQgdmFsdWUgaXMgY2FsY3VsYXRlZC5cbiAgICpcbiAgICogQHJldHVybnMgQSBjYWxjdWxhdGVkIGRlZmF1bHQgSlNPTiB2YWx1ZSBmb3IgYSBzcGVjaWZpYyBzZXR0aW5nLlxuICAgKi9cbiAgZGVmYXVsdChrZXk6IHN0cmluZyk6IFBhcnRpYWxKU09OVmFsdWUgfCB1bmRlZmluZWQge1xuICAgIHJldHVybiBQcml2YXRlLnJlaWZ5RGVmYXVsdCh0aGlzLnNjaGVtYSwga2V5KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBEaXNwb3NlIG9mIHRoZSBwbHVnaW4gc2V0dGluZ3MgcmVzb3VyY2VzLlxuICAgKi9cbiAgZGlzcG9zZSgpOiB2b2lkIHtcbiAgICBpZiAodGhpcy5faXNEaXNwb3NlZCkge1xuICAgICAgcmV0dXJuO1xuICAgIH1cblxuICAgIHRoaXMuX2lzRGlzcG9zZWQgPSB0cnVlO1xuICAgIFNpZ25hbC5jbGVhckRhdGEodGhpcyk7XG4gIH1cblxuICAvKipcbiAgICogR2V0IGFuIGluZGl2aWR1YWwgc2V0dGluZy5cbiAgICpcbiAgICogQHBhcmFtIGtleSAtIFRoZSBuYW1lIG9mIHRoZSBzZXR0aW5nIGJlaW5nIHJldHJpZXZlZC5cbiAgICpcbiAgICogQHJldHVybnMgVGhlIHNldHRpbmcgdmFsdWUuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogVGhpcyBtZXRob2QgcmV0dXJucyBzeW5jaHJvbm91c2x5IGJlY2F1c2UgaXQgdXNlcyBhIGNhY2hlZCBjb3B5IG9mIHRoZVxuICAgKiBwbHVnaW4gc2V0dGluZ3MgdGhhdCBpcyBzeW5jaHJvbml6ZWQgd2l0aCB0aGUgcmVnaXN0cnkuXG4gICAqL1xuICBnZXQoXG4gICAga2V5OiBzdHJpbmdcbiAgKToge1xuICAgIGNvbXBvc2l0ZTogUmVhZG9ubHlQYXJ0aWFsSlNPTlZhbHVlIHwgdW5kZWZpbmVkO1xuICAgIHVzZXI6IFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZSB8IHVuZGVmaW5lZDtcbiAgfSB7XG4gICAgY29uc3QgeyBjb21wb3NpdGUsIHVzZXIgfSA9IHRoaXM7XG5cbiAgICByZXR1cm4ge1xuICAgICAgY29tcG9zaXRlOlxuICAgICAgICBjb21wb3NpdGVba2V5XSAhPT0gdW5kZWZpbmVkID8gY29weShjb21wb3NpdGVba2V5XSEpIDogdW5kZWZpbmVkLFxuICAgICAgdXNlcjogdXNlcltrZXldICE9PSB1bmRlZmluZWQgPyBjb3B5KHVzZXJba2V5XSEpIDogdW5kZWZpbmVkXG4gICAgfTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZW1vdmUgYSBzaW5nbGUgc2V0dGluZy5cbiAgICpcbiAgICogQHBhcmFtIGtleSAtIFRoZSBuYW1lIG9mIHRoZSBzZXR0aW5nIGJlaW5nIHJlbW92ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIHNldHRpbmcgaXMgcmVtb3ZlZC5cbiAgICpcbiAgICogIyMjIyBOb3Rlc1xuICAgKiBUaGlzIGZ1bmN0aW9uIGlzIGFzeW5jaHJvbm91cyBiZWNhdXNlIGl0IHdyaXRlcyB0byB0aGUgc2V0dGluZyByZWdpc3RyeS5cbiAgICovXG4gIHJlbW92ZShrZXk6IHN0cmluZyk6IFByb21pc2U8dm9pZD4ge1xuICAgIHJldHVybiB0aGlzLnJlZ2lzdHJ5LnJlbW92ZSh0aGlzLnBsdWdpbi5pZCwga2V5KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTYXZlIGFsbCBvZiB0aGUgcGx1Z2luJ3MgdXNlciBzZXR0aW5ncyBhdCBvbmNlLlxuICAgKi9cbiAgc2F2ZShyYXc6IHN0cmluZyk6IFByb21pc2U8dm9pZD4ge1xuICAgIHJldHVybiB0aGlzLnJlZ2lzdHJ5LnVwbG9hZCh0aGlzLnBsdWdpbi5pZCwgcmF3KTtcbiAgfVxuXG4gIC8qKlxuICAgKiBTZXQgYSBzaW5nbGUgc2V0dGluZy5cbiAgICpcbiAgICogQHBhcmFtIGtleSAtIFRoZSBuYW1lIG9mIHRoZSBzZXR0aW5nIGJlaW5nIHNldC5cbiAgICpcbiAgICogQHBhcmFtIHZhbHVlIC0gVGhlIHZhbHVlIG9mIHRoZSBzZXR0aW5nLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIHByb21pc2UgdGhhdCByZXNvbHZlcyB3aGVuIHRoZSBzZXR0aW5nIGhhcyBiZWVuIHNhdmVkLlxuICAgKlxuICAgKiAjIyMjIE5vdGVzXG4gICAqIFRoaXMgZnVuY3Rpb24gaXMgYXN5bmNocm9ub3VzIGJlY2F1c2UgaXQgd3JpdGVzIHRvIHRoZSBzZXR0aW5nIHJlZ2lzdHJ5LlxuICAgKi9cbiAgc2V0KGtleTogc3RyaW5nLCB2YWx1ZTogSlNPTlZhbHVlKTogUHJvbWlzZTx2b2lkPiB7XG4gICAgcmV0dXJuIHRoaXMucmVnaXN0cnkuc2V0KHRoaXMucGx1Z2luLmlkLCBrZXksIHZhbHVlKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBWYWxpZGF0ZXMgcmF3IHNldHRpbmdzIHdpdGggY29tbWVudHMuXG4gICAqXG4gICAqIEBwYXJhbSByYXcgLSBUaGUgSlNPTiB3aXRoIGNvbW1lbnRzIHN0cmluZyBiZWluZyB2YWxpZGF0ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgbGlzdCBvZiBlcnJvcnMgb3IgYG51bGxgIGlmIHZhbGlkLlxuICAgKi9cbiAgdmFsaWRhdGUocmF3OiBzdHJpbmcpOiBJU2NoZW1hVmFsaWRhdG9yLklFcnJvcltdIHwgbnVsbCB7XG4gICAgY29uc3QgZGF0YSA9IHsgY29tcG9zaXRlOiB7fSwgdXNlcjoge30gfTtcbiAgICBjb25zdCB7IGlkLCBzY2hlbWEgfSA9IHRoaXMucGx1Z2luO1xuICAgIGNvbnN0IHZhbGlkYXRvciA9IHRoaXMucmVnaXN0cnkudmFsaWRhdG9yO1xuICAgIGNvbnN0IHZlcnNpb24gPSB0aGlzLnZlcnNpb247XG5cbiAgICByZXR1cm4gdmFsaWRhdG9yLnZhbGlkYXRlRGF0YSh7IGRhdGEsIGlkLCByYXcsIHNjaGVtYSwgdmVyc2lvbiB9LCBmYWxzZSk7XG4gIH1cblxuICAvKipcbiAgICogSGFuZGxlIHBsdWdpbiBjaGFuZ2VzIGluIHRoZSBzZXR0aW5nIHJlZ2lzdHJ5LlxuICAgKi9cbiAgcHJpdmF0ZSBfb25QbHVnaW5DaGFuZ2VkKHNlbmRlcjogYW55LCBwbHVnaW46IHN0cmluZyk6IHZvaWQge1xuICAgIGlmIChwbHVnaW4gPT09IHRoaXMucGx1Z2luLmlkKSB7XG4gICAgICB0aGlzLl9jaGFuZ2VkLmVtaXQodW5kZWZpbmVkKTtcbiAgICB9XG4gIH1cblxuICBwcml2YXRlIF9jaGFuZ2VkID0gbmV3IFNpZ25hbDx0aGlzLCB2b2lkPih0aGlzKTtcbiAgcHJpdmF0ZSBfaXNEaXNwb3NlZCA9IGZhbHNlO1xufVxuXG4vKipcbiAqIEEgbmFtZXNwYWNlIGZvciBgU2V0dGluZ1JlZ2lzdHJ5YCBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIFNldHRpbmdSZWdpc3RyeSB7XG4gIC8qKlxuICAgKiBUaGUgaW5zdGFudGlhdGlvbiBvcHRpb25zIGZvciBhIHNldHRpbmcgcmVnaXN0cnlcbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSU9wdGlvbnMge1xuICAgIC8qKlxuICAgICAqIFRoZSBkYXRhIGNvbm5lY3RvciB1c2VkIGJ5IHRoZSBzZXR0aW5nIHJlZ2lzdHJ5LlxuICAgICAqL1xuICAgIGNvbm5lY3RvcjogSURhdGFDb25uZWN0b3I8SVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luLCBzdHJpbmc+O1xuXG4gICAgLyoqXG4gICAgICogUHJlbG9hZGVkIHBsdWdpbiBkYXRhIHRvIHBvcHVsYXRlIHRoZSBzZXR0aW5nIHJlZ2lzdHJ5LlxuICAgICAqL1xuICAgIHBsdWdpbnM/OiBJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW5bXTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBudW1iZXIgb2YgbWlsbGlzZWNvbmRzIGJlZm9yZSBhIGBsb2FkKClgIGNhbGwgdG8gdGhlIHJlZ2lzdHJ5IHdhaXRzXG4gICAgICogYmVmb3JlIHRpbWluZyBvdXQgaWYgaXQgcmVxdWlyZXMgYSB0cmFuc2Zvcm1hdGlvbiB0aGF0IGhhcyBub3QgYmVlblxuICAgICAqIHJlZ2lzdGVyZWQuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogVGhlIGRlZmF1bHQgdmFsdWUgaXMgNzAwMC5cbiAgICAgKi9cbiAgICB0aW1lb3V0PzogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHZhbGlkYXRvciB1c2VkIHRvIGVuZm9yY2UgdGhlIHNldHRpbmdzIEpTT04gc2NoZW1hLlxuICAgICAqL1xuICAgIHZhbGlkYXRvcj86IElTY2hlbWFWYWxpZGF0b3I7XG4gIH1cblxuICAvKipcbiAgICogUmVjb25jaWxlIHRoZSBtZW51cy5cbiAgICpcbiAgICogQHBhcmFtIHJlZmVyZW5jZSBUaGUgcmVmZXJlbmNlIGxpc3Qgb2YgbWVudXMuXG4gICAqIEBwYXJhbSBhZGRpdGlvbiBUaGUgbGlzdCBvZiBtZW51cyB0byBhZGQuXG4gICAqIEBwYXJhbSB3YXJuIFdhcm4gaWYgdGhlIGNvbW1hbmQgaXRlbXMgYXJlIGR1cGxpY2F0ZWQgd2l0aGluIHRoZSBzYW1lIG1lbnUuXG4gICAqIEByZXR1cm5zIFRoZSByZWNvbmNpbGVkIGxpc3Qgb2YgbWVudXMuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gcmVjb25jaWxlTWVudXMoXG4gICAgcmVmZXJlbmNlOiBJU2V0dGluZ1JlZ2lzdHJ5LklNZW51W10gfCBudWxsLFxuICAgIGFkZGl0aW9uOiBJU2V0dGluZ1JlZ2lzdHJ5LklNZW51W10gfCBudWxsLFxuICAgIHdhcm46IGJvb2xlYW4gPSBmYWxzZSxcbiAgICBhZGROZXdJdGVtczogYm9vbGVhbiA9IHRydWVcbiAgKTogSVNldHRpbmdSZWdpc3RyeS5JTWVudVtdIHtcbiAgICBpZiAoIXJlZmVyZW5jZSkge1xuICAgICAgcmV0dXJuIGFkZGl0aW9uICYmIGFkZE5ld0l0ZW1zID8gSlNPTkV4dC5kZWVwQ29weShhZGRpdGlvbikgOiBbXTtcbiAgICB9XG4gICAgaWYgKCFhZGRpdGlvbikge1xuICAgICAgcmV0dXJuIEpTT05FeHQuZGVlcENvcHkocmVmZXJlbmNlKTtcbiAgICB9XG5cbiAgICBjb25zdCBtZXJnZWQgPSBKU09ORXh0LmRlZXBDb3B5KHJlZmVyZW5jZSk7XG5cbiAgICBhZGRpdGlvbi5mb3JFYWNoKG1lbnUgPT4ge1xuICAgICAgY29uc3QgcmVmSW5kZXggPSBtZXJnZWQuZmluZEluZGV4KHJlZiA9PiByZWYuaWQgPT09IG1lbnUuaWQpO1xuICAgICAgaWYgKHJlZkluZGV4ID49IDApIHtcbiAgICAgICAgbWVyZ2VkW3JlZkluZGV4XSA9IHtcbiAgICAgICAgICAuLi5tZXJnZWRbcmVmSW5kZXhdLFxuICAgICAgICAgIC4uLm1lbnUsXG4gICAgICAgICAgaXRlbXM6IHJlY29uY2lsZUl0ZW1zKFxuICAgICAgICAgICAgbWVyZ2VkW3JlZkluZGV4XS5pdGVtcyxcbiAgICAgICAgICAgIG1lbnUuaXRlbXMsXG4gICAgICAgICAgICB3YXJuLFxuICAgICAgICAgICAgYWRkTmV3SXRlbXNcbiAgICAgICAgICApXG4gICAgICAgIH07XG4gICAgICB9IGVsc2Uge1xuICAgICAgICBpZiAoYWRkTmV3SXRlbXMpIHtcbiAgICAgICAgICBtZXJnZWQucHVzaChtZW51KTtcbiAgICAgICAgfVxuICAgICAgfVxuICAgIH0pO1xuXG4gICAgcmV0dXJuIG1lcmdlZDtcbiAgfVxuXG4gIC8qKlxuICAgKiBNZXJnZSB0d28gc2V0IG9mIG1lbnUgaXRlbXMuXG4gICAqXG4gICAqIEBwYXJhbSByZWZlcmVuY2UgUmVmZXJlbmNlIHNldCBvZiBtZW51IGl0ZW1zXG4gICAqIEBwYXJhbSBhZGRpdGlvbiBOZXcgaXRlbXMgdG8gYWRkXG4gICAqIEBwYXJhbSB3YXJuIFdoZXRoZXIgdG8gd2FybiBpZiBpdGVtIGlzIGR1cGxpY2F0ZWQ7IGRlZmF1bHQgdG8gZmFsc2VcbiAgICogQHJldHVybnMgVGhlIG1lcmdlZCBzZXQgb2YgaXRlbXNcbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiByZWNvbmNpbGVJdGVtczxUIGV4dGVuZHMgSVNldHRpbmdSZWdpc3RyeS5JTWVudUl0ZW0+KFxuICAgIHJlZmVyZW5jZT86IFRbXSxcbiAgICBhZGRpdGlvbj86IFRbXSxcbiAgICB3YXJuOiBib29sZWFuID0gZmFsc2UsXG4gICAgYWRkTmV3SXRlbXM6IGJvb2xlYW4gPSB0cnVlXG4gICk6IFRbXSB8IHVuZGVmaW5lZCB7XG4gICAgaWYgKCFyZWZlcmVuY2UpIHtcbiAgICAgIHJldHVybiBhZGRpdGlvbiA/IEpTT05FeHQuZGVlcENvcHkoYWRkaXRpb24pIDogdW5kZWZpbmVkO1xuICAgIH1cbiAgICBpZiAoIWFkZGl0aW9uKSB7XG4gICAgICByZXR1cm4gSlNPTkV4dC5kZWVwQ29weShyZWZlcmVuY2UpO1xuICAgIH1cblxuICAgIGNvbnN0IGl0ZW1zID0gSlNPTkV4dC5kZWVwQ29weShyZWZlcmVuY2UpO1xuXG4gICAgLy8gTWVyZ2UgYXJyYXkgZWxlbWVudCBkZXBlbmRpbmcgb24gdGhlIHR5cGVcbiAgICBhZGRpdGlvbi5mb3JFYWNoKGl0ZW0gPT4ge1xuICAgICAgc3dpdGNoIChpdGVtLnR5cGUgPz8gJ2NvbW1hbmQnKSB7XG4gICAgICAgIGNhc2UgJ3NlcGFyYXRvcic6XG4gICAgICAgICAgaWYgKGFkZE5ld0l0ZW1zKSB7XG4gICAgICAgICAgICBpdGVtcy5wdXNoKHsgLi4uaXRlbSB9KTtcbiAgICAgICAgICB9XG4gICAgICAgICAgYnJlYWs7XG4gICAgICAgIGNhc2UgJ3N1Ym1lbnUnOlxuICAgICAgICAgIGlmIChpdGVtLnN1Ym1lbnUpIHtcbiAgICAgICAgICAgIGNvbnN0IHJlZkluZGV4ID0gaXRlbXMuZmluZEluZGV4KFxuICAgICAgICAgICAgICByZWYgPT5cbiAgICAgICAgICAgICAgICByZWYudHlwZSA9PT0gJ3N1Ym1lbnUnICYmIHJlZi5zdWJtZW51Py5pZCA9PT0gaXRlbS5zdWJtZW51Py5pZFxuICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIGlmIChyZWZJbmRleCA8IDApIHtcbiAgICAgICAgICAgICAgaWYgKGFkZE5ld0l0ZW1zKSB7XG4gICAgICAgICAgICAgICAgaXRlbXMucHVzaChKU09ORXh0LmRlZXBDb3B5KGl0ZW0pKTtcbiAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgaXRlbXNbcmVmSW5kZXhdID0ge1xuICAgICAgICAgICAgICAgIC4uLml0ZW1zW3JlZkluZGV4XSxcbiAgICAgICAgICAgICAgICAuLi5pdGVtLFxuICAgICAgICAgICAgICAgIHN1Ym1lbnU6IHJlY29uY2lsZU1lbnVzKFxuICAgICAgICAgICAgICAgICAgaXRlbXNbcmVmSW5kZXhdLnN1Ym1lbnVcbiAgICAgICAgICAgICAgICAgICAgPyBbaXRlbXNbcmVmSW5kZXhdLnN1Ym1lbnUgYXMgYW55XVxuICAgICAgICAgICAgICAgICAgICA6IG51bGwsXG4gICAgICAgICAgICAgICAgICBbaXRlbS5zdWJtZW51XSxcbiAgICAgICAgICAgICAgICAgIHdhcm4sXG4gICAgICAgICAgICAgICAgICBhZGROZXdJdGVtc1xuICAgICAgICAgICAgICAgIClbMF1cbiAgICAgICAgICAgICAgfTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9XG4gICAgICAgICAgYnJlYWs7XG4gICAgICAgIGNhc2UgJ2NvbW1hbmQnOlxuICAgICAgICAgIGlmIChpdGVtLmNvbW1hbmQpIHtcbiAgICAgICAgICAgIGNvbnN0IHJlZkluZGV4ID0gaXRlbXMuZmluZEluZGV4KFxuICAgICAgICAgICAgICByZWYgPT5cbiAgICAgICAgICAgICAgICByZWYuY29tbWFuZCA9PT0gaXRlbS5jb21tYW5kICYmXG4gICAgICAgICAgICAgICAgcmVmLnNlbGVjdG9yID09PSBpdGVtLnNlbGVjdG9yICYmXG4gICAgICAgICAgICAgICAgSlNPTkV4dC5kZWVwRXF1YWwocmVmLmFyZ3MgPz8ge30sIGl0ZW0uYXJncyA/PyB7fSlcbiAgICAgICAgICAgICk7XG4gICAgICAgICAgICBpZiAocmVmSW5kZXggPCAwKSB7XG4gICAgICAgICAgICAgIGlmIChhZGROZXdJdGVtcykge1xuICAgICAgICAgICAgICAgIGl0ZW1zLnB1c2goeyAuLi5pdGVtIH0pO1xuICAgICAgICAgICAgICB9XG4gICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICBpZiAod2Fybikge1xuICAgICAgICAgICAgICAgIGNvbnNvbGUud2FybihcbiAgICAgICAgICAgICAgICAgIGBNZW51IGVudHJ5IGZvciBjb21tYW5kICcke2l0ZW0uY29tbWFuZH0nIGlzIGR1cGxpY2F0ZWQuYFxuICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgaXRlbXNbcmVmSW5kZXhdID0geyAuLi5pdGVtc1tyZWZJbmRleF0sIC4uLml0ZW0gfTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgICB9XG4gICAgICB9XG4gICAgfSk7XG5cbiAgICByZXR1cm4gaXRlbXM7XG4gIH1cblxuICBleHBvcnQgZnVuY3Rpb24gZmlsdGVyRGlzYWJsZWRJdGVtczxUIGV4dGVuZHMgSVNldHRpbmdSZWdpc3RyeS5JTWVudUl0ZW0+KFxuICAgIGl0ZW1zOiBUW11cbiAgKTogVFtdIHtcbiAgICByZXR1cm4gaXRlbXMucmVkdWNlPFRbXT4oKGZpbmFsLCB2YWx1ZSkgPT4ge1xuICAgICAgY29uc3QgY29weSA9IHsgLi4udmFsdWUgfTtcbiAgICAgIGlmICghY29weS5kaXNhYmxlZCkge1xuICAgICAgICBpZiAoY29weS50eXBlID09PSAnc3VibWVudScpIHtcbiAgICAgICAgICBjb25zdCB7IHN1Ym1lbnUgfSA9IGNvcHk7XG4gICAgICAgICAgaWYgKHN1Ym1lbnUgJiYgIXN1Ym1lbnUuZGlzYWJsZWQpIHtcbiAgICAgICAgICAgIGNvcHkuc3VibWVudSA9IHtcbiAgICAgICAgICAgICAgLi4uc3VibWVudSxcbiAgICAgICAgICAgICAgaXRlbXM6IGZpbHRlckRpc2FibGVkSXRlbXMoc3VibWVudS5pdGVtcyA/PyBbXSlcbiAgICAgICAgICAgIH07XG4gICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIGZpbmFsLnB1c2goY29weSk7XG4gICAgICB9XG5cbiAgICAgIHJldHVybiBmaW5hbDtcbiAgICB9LCBbXSk7XG4gIH1cblxuICAvKipcbiAgICogUmVjb25jaWxlIGRlZmF1bHQgYW5kIHVzZXIgc2hvcnRjdXRzIGFuZCByZXR1cm4gdGhlIGNvbXBvc2l0ZSBsaXN0LlxuICAgKlxuICAgKiBAcGFyYW0gZGVmYXVsdHMgLSBUaGUgbGlzdCBvZiBkZWZhdWx0IHNob3J0Y3V0cy5cbiAgICpcbiAgICogQHBhcmFtIHVzZXIgLSBUaGUgbGlzdCBvZiB1c2VyIHNob3J0Y3V0IG92ZXJyaWRlcyBhbmQgYWRkaXRpb25zLlxuICAgKlxuICAgKiBAcmV0dXJucyBBIGxvYWRhYmxlIGxpc3Qgb2Ygc2hvcnRjdXRzIChvbWl0dGluZyBkaXNhYmxlZCBhbmQgb3ZlcnJpZGRlbikuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gcmVjb25jaWxlU2hvcnRjdXRzKFxuICAgIGRlZmF1bHRzOiBJU2V0dGluZ1JlZ2lzdHJ5LklTaG9ydGN1dFtdLFxuICAgIHVzZXI6IElTZXR0aW5nUmVnaXN0cnkuSVNob3J0Y3V0W11cbiAgKTogSVNldHRpbmdSZWdpc3RyeS5JU2hvcnRjdXRbXSB7XG4gICAgY29uc3QgbWVtbzoge1xuICAgICAgW2tleXM6IHN0cmluZ106IHtcbiAgICAgICAgW3NlbGVjdG9yOiBzdHJpbmddOiBib29sZWFuOyAvLyBJZiBgdHJ1ZWAsIHNob3VsZCB3YXJuIGlmIGEgZGVmYXVsdCBzaG9ydGN1dCBjb25mbGljdHMuXG4gICAgICB9O1xuICAgIH0gPSB7fTtcblxuICAgIC8vIElmIGEgdXNlciBzaG9ydGN1dCBjb2xsaWRlcyB3aXRoIGFub3RoZXIgdXNlciBzaG9ydGN1dCB3YXJuIGFuZCBmaWx0ZXIuXG4gICAgdXNlciA9IHVzZXIuZmlsdGVyKHNob3J0Y3V0ID0+IHtcbiAgICAgIGNvbnN0IGtleXMgPSBDb21tYW5kUmVnaXN0cnkubm9ybWFsaXplS2V5cyhzaG9ydGN1dCkuam9pbihcbiAgICAgICAgUkVDT1JEX1NFUEFSQVRPUlxuICAgICAgKTtcbiAgICAgIGlmICgha2V5cykge1xuICAgICAgICBjb25zb2xlLndhcm4oXG4gICAgICAgICAgJ1NraXBwaW5nIHRoaXMgc2hvcnRjdXQgYmVjYXVzZSB0aGVyZSBhcmUgbm8gYWN0aW9uYWJsZSBrZXlzIG9uIHRoaXMgcGxhdGZvcm0nLFxuICAgICAgICAgIHNob3J0Y3V0XG4gICAgICAgICk7XG4gICAgICAgIHJldHVybiBmYWxzZTtcbiAgICAgIH1cbiAgICAgIGlmICghKGtleXMgaW4gbWVtbykpIHtcbiAgICAgICAgbWVtb1trZXlzXSA9IHt9O1xuICAgICAgfVxuXG4gICAgICBjb25zdCB7IHNlbGVjdG9yIH0gPSBzaG9ydGN1dDtcbiAgICAgIGlmICghKHNlbGVjdG9yIGluIG1lbW9ba2V5c10pKSB7XG4gICAgICAgIG1lbW9ba2V5c11bc2VsZWN0b3JdID0gZmFsc2U7IC8vIERvIG5vdCB3YXJuIGlmIGEgZGVmYXVsdCBzaG9ydGN1dCBjb25mbGljdHMuXG4gICAgICAgIHJldHVybiB0cnVlO1xuICAgICAgfVxuXG4gICAgICBjb25zb2xlLndhcm4oXG4gICAgICAgICdTa2lwcGluZyB0aGlzIHNob3J0Y3V0IGJlY2F1c2UgaXQgY29sbGlkZXMgd2l0aCBhbm90aGVyIHNob3J0Y3V0LicsXG4gICAgICAgIHNob3J0Y3V0XG4gICAgICApO1xuICAgICAgcmV0dXJuIGZhbHNlO1xuICAgIH0pO1xuXG4gICAgLy8gSWYgYSBkZWZhdWx0IHNob3J0Y3V0IGNvbGxpZGVzIHdpdGggYW5vdGhlciBkZWZhdWx0LCB3YXJuIGFuZCBmaWx0ZXIsXG4gICAgLy8gdW5sZXNzIG9uZSBvZiB0aGUgc2hvcnRjdXRzIGlzIGEgZGlzYWJsaW5nIHNob3J0Y3V0IChzbyBsb29rIHRocm91Z2hcbiAgICAvLyBkaXNhYmxlZCBzaG9ydGN1dHMgZmlyc3QpLiBJZiBhIHNob3J0Y3V0IGhhcyBhbHJlYWR5IGJlZW4gYWRkZWQgYnkgdGhlXG4gICAgLy8gdXNlciBwcmVmZXJlbmNlcywgZmlsdGVyIGl0IG91dCB0b28gKHRoaXMgaW5jbHVkZXMgc2hvcnRjdXRzIHRoYXQgYXJlXG4gICAgLy8gZGlzYWJsZWQgYnkgdXNlciBwcmVmZXJlbmNlcykuXG4gICAgZGVmYXVsdHMgPSBbXG4gICAgICAuLi5kZWZhdWx0cy5maWx0ZXIocyA9PiAhIXMuZGlzYWJsZWQpLFxuICAgICAgLi4uZGVmYXVsdHMuZmlsdGVyKHMgPT4gIXMuZGlzYWJsZWQpXG4gICAgXS5maWx0ZXIoc2hvcnRjdXQgPT4ge1xuICAgICAgY29uc3Qga2V5cyA9IENvbW1hbmRSZWdpc3RyeS5ub3JtYWxpemVLZXlzKHNob3J0Y3V0KS5qb2luKFxuICAgICAgICBSRUNPUkRfU0VQQVJBVE9SXG4gICAgICApO1xuXG4gICAgICBpZiAoIWtleXMpIHtcbiAgICAgICAgcmV0dXJuIGZhbHNlO1xuICAgICAgfVxuICAgICAgaWYgKCEoa2V5cyBpbiBtZW1vKSkge1xuICAgICAgICBtZW1vW2tleXNdID0ge307XG4gICAgICB9XG5cbiAgICAgIGNvbnN0IHsgZGlzYWJsZWQsIHNlbGVjdG9yIH0gPSBzaG9ydGN1dDtcbiAgICAgIGlmICghKHNlbGVjdG9yIGluIG1lbW9ba2V5c10pKSB7XG4gICAgICAgIC8vIFdhcm4gb2YgZnV0dXJlIGNvbmZsaWN0cyBpZiB0aGUgZGVmYXVsdCBzaG9ydGN1dCBpcyBub3QgZGlzYWJsZWQuXG4gICAgICAgIG1lbW9ba2V5c11bc2VsZWN0b3JdID0gIWRpc2FibGVkO1xuICAgICAgICByZXR1cm4gdHJ1ZTtcbiAgICAgIH1cblxuICAgICAgLy8gV2UgaGF2ZSBhIGNvbmZsaWN0IG5vdy4gV2FybiB0aGUgdXNlciBpZiB3ZSBuZWVkIHRvIGRvIHNvLlxuICAgICAgaWYgKG1lbW9ba2V5c11bc2VsZWN0b3JdKSB7XG4gICAgICAgIGNvbnNvbGUud2FybihcbiAgICAgICAgICAnU2tpcHBpbmcgdGhpcyBkZWZhdWx0IHNob3J0Y3V0IGJlY2F1c2UgaXQgY29sbGlkZXMgd2l0aCBhbm90aGVyIGRlZmF1bHQgc2hvcnRjdXQuJyxcbiAgICAgICAgICBzaG9ydGN1dFxuICAgICAgICApO1xuICAgICAgfVxuXG4gICAgICByZXR1cm4gZmFsc2U7XG4gICAgfSk7XG5cbiAgICAvLyBSZXR1cm4gYWxsIHRoZSBzaG9ydGN1dHMgdGhhdCBzaG91bGQgYmUgcmVnaXN0ZXJlZFxuICAgIHJldHVybiB1c2VyLmNvbmNhdChkZWZhdWx0cykuZmlsdGVyKHNob3J0Y3V0ID0+ICFzaG9ydGN1dC5kaXNhYmxlZCk7XG4gIH1cbn1cblxuLyoqXG4gKiBBIG5hbWVzcGFjZSBmb3IgYFNldHRpbmdzYCBzdGF0aWNzLlxuICovXG5leHBvcnQgbmFtZXNwYWNlIFNldHRpbmdzIHtcbiAgLyoqXG4gICAqIFRoZSBpbnN0YW50aWF0aW9uIG9wdGlvbnMgZm9yIGEgYFNldHRpbmdzYCBvYmplY3QuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElPcHRpb25zIHtcbiAgICAvKipcbiAgICAgKiBUaGUgc2V0dGluZyB2YWx1ZXMgZm9yIGEgcGx1Z2luLlxuICAgICAqL1xuICAgIHBsdWdpbjogSVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHN5c3RlbSByZWdpc3RyeSBpbnN0YW5jZSB1c2VkIGJ5IHRoZSBzZXR0aW5ncyBtYW5hZ2VyLlxuICAgICAqL1xuICAgIHJlZ2lzdHJ5OiBJU2V0dGluZ1JlZ2lzdHJ5O1xuICB9XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgbW9kdWxlIGRhdGEuXG4gKi9cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgLyoqXG4gICAqIFRoZSBkZWZhdWx0IGluZGVudGF0aW9uIGxldmVsLCB1c2VzIHNwYWNlcyBpbnN0ZWFkIG9mIHRhYnMuXG4gICAqL1xuICBjb25zdCBpbmRlbnQgPSAnICAgICc7XG5cbiAgLyoqXG4gICAqIFJlcGxhY2VtZW50IHRleHQgZm9yIHNjaGVtYSBwcm9wZXJ0aWVzIG1pc3NpbmcgYSBgZGVzY3JpcHRpb25gIGZpZWxkLlxuICAgKi9cbiAgY29uc3Qgbm9uZGVzY3JpcHQgPSAnW21pc3Npbmcgc2NoZW1hIGRlc2NyaXB0aW9uXSc7XG5cbiAgLyoqXG4gICAqIFJlcGxhY2VtZW50IHRleHQgZm9yIHNjaGVtYSBwcm9wZXJ0aWVzIG1pc3NpbmcgYSBgdGl0bGVgIGZpZWxkLlxuICAgKi9cbiAgY29uc3QgdW50aXRsZWQgPSAnW21pc3Npbmcgc2NoZW1hIHRpdGxlXSc7XG5cbiAgLyoqXG4gICAqIFJldHVybnMgYW4gYW5ub3RhdGVkIChKU09OIHdpdGggY29tbWVudHMpIHZlcnNpb24gb2YgYSBzY2hlbWEncyBkZWZhdWx0cy5cbiAgICovXG4gIGV4cG9ydCBmdW5jdGlvbiBhbm5vdGF0ZWREZWZhdWx0cyhcbiAgICBzY2hlbWE6IElTZXR0aW5nUmVnaXN0cnkuSVNjaGVtYSxcbiAgICBwbHVnaW46IHN0cmluZ1xuICApOiBzdHJpbmcge1xuICAgIGNvbnN0IHsgZGVzY3JpcHRpb24sIHByb3BlcnRpZXMsIHRpdGxlIH0gPSBzY2hlbWE7XG4gICAgY29uc3Qga2V5cyA9IHByb3BlcnRpZXNcbiAgICAgID8gT2JqZWN0LmtleXMocHJvcGVydGllcykuc29ydCgoYSwgYikgPT4gYS5sb2NhbGVDb21wYXJlKGIpKVxuICAgICAgOiBbXTtcbiAgICBjb25zdCBsZW5ndGggPSBNYXRoLm1heCgoZGVzY3JpcHRpb24gfHwgbm9uZGVzY3JpcHQpLmxlbmd0aCwgcGx1Z2luLmxlbmd0aCk7XG5cbiAgICByZXR1cm4gW1xuICAgICAgJ3snLFxuICAgICAgcHJlZml4KGAke3RpdGxlIHx8IHVudGl0bGVkfWApLFxuICAgICAgcHJlZml4KHBsdWdpbiksXG4gICAgICBwcmVmaXgoZGVzY3JpcHRpb24gfHwgbm9uZGVzY3JpcHQpLFxuICAgICAgcHJlZml4KCcqJy5yZXBlYXQobGVuZ3RoKSksXG4gICAgICAnJyxcbiAgICAgIGpvaW4oa2V5cy5tYXAoa2V5ID0+IGRlZmF1bHREb2N1bWVudGVkVmFsdWUoc2NoZW1hLCBrZXkpKSksXG4gICAgICAnfSdcbiAgICBdLmpvaW4oJ1xcbicpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJldHVybnMgYW4gYW5ub3RhdGVkIChKU09OIHdpdGggY29tbWVudHMpIHZlcnNpb24gb2YgYSBwbHVnaW4nc1xuICAgKiBzZXR0aW5nIGRhdGEuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gYW5ub3RhdGVkUGx1Z2luKFxuICAgIHBsdWdpbjogSVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luLFxuICAgIGRhdGE6IEpTT05PYmplY3RcbiAgKTogc3RyaW5nIHtcbiAgICBjb25zdCB7IGRlc2NyaXB0aW9uLCB0aXRsZSB9ID0gcGx1Z2luLnNjaGVtYTtcbiAgICBjb25zdCBrZXlzID0gT2JqZWN0LmtleXMoZGF0YSkuc29ydCgoYSwgYikgPT4gYS5sb2NhbGVDb21wYXJlKGIpKTtcbiAgICBjb25zdCBsZW5ndGggPSBNYXRoLm1heChcbiAgICAgIChkZXNjcmlwdGlvbiB8fCBub25kZXNjcmlwdCkubGVuZ3RoLFxuICAgICAgcGx1Z2luLmlkLmxlbmd0aFxuICAgICk7XG5cbiAgICByZXR1cm4gW1xuICAgICAgJ3snLFxuICAgICAgcHJlZml4KGAke3RpdGxlIHx8IHVudGl0bGVkfWApLFxuICAgICAgcHJlZml4KHBsdWdpbi5pZCksXG4gICAgICBwcmVmaXgoZGVzY3JpcHRpb24gfHwgbm9uZGVzY3JpcHQpLFxuICAgICAgcHJlZml4KCcqJy5yZXBlYXQobGVuZ3RoKSksXG4gICAgICAnJyxcbiAgICAgIGpvaW4oa2V5cy5tYXAoa2V5ID0+IGRvY3VtZW50ZWRWYWx1ZShwbHVnaW4uc2NoZW1hLCBrZXksIGRhdGFba2V5XSkpKSxcbiAgICAgICd9J1xuICAgIF0uam9pbignXFxuJyk7XG4gIH1cblxuICAvKipcbiAgICogUmV0dXJucyB0aGUgZGVmYXVsdCB2YWx1ZS13aXRoLWRvY3VtZW50YXRpb24tc3RyaW5nIGZvciBhXG4gICAqIHNwZWNpZmljIHNjaGVtYSBwcm9wZXJ0eS5cbiAgICovXG4gIGZ1bmN0aW9uIGRlZmF1bHREb2N1bWVudGVkVmFsdWUoXG4gICAgc2NoZW1hOiBJU2V0dGluZ1JlZ2lzdHJ5LklTY2hlbWEsXG4gICAga2V5OiBzdHJpbmdcbiAgKTogc3RyaW5nIHtcbiAgICBjb25zdCBwcm9wcyA9IChzY2hlbWEucHJvcGVydGllcyAmJiBzY2hlbWEucHJvcGVydGllc1trZXldKSB8fCB7fTtcbiAgICBjb25zdCB0eXBlID0gcHJvcHNbJ3R5cGUnXTtcbiAgICBjb25zdCBkZXNjcmlwdGlvbiA9IHByb3BzWydkZXNjcmlwdGlvbiddIHx8IG5vbmRlc2NyaXB0O1xuICAgIGNvbnN0IHRpdGxlID0gcHJvcHNbJ3RpdGxlJ10gfHwgJyc7XG4gICAgY29uc3QgcmVpZmllZCA9IHJlaWZ5RGVmYXVsdChzY2hlbWEsIGtleSk7XG4gICAgY29uc3Qgc3BhY2VzID0gaW5kZW50Lmxlbmd0aDtcbiAgICBjb25zdCBkZWZhdWx0cyA9XG4gICAgICByZWlmaWVkICE9PSB1bmRlZmluZWRcbiAgICAgICAgPyBwcmVmaXgoYFwiJHtrZXl9XCI6ICR7SlNPTi5zdHJpbmdpZnkocmVpZmllZCwgbnVsbCwgc3BhY2VzKX1gLCBpbmRlbnQpXG4gICAgICAgIDogcHJlZml4KGBcIiR7a2V5fVwiOiAke3R5cGV9YCk7XG5cbiAgICByZXR1cm4gW3ByZWZpeCh0aXRsZSksIHByZWZpeChkZXNjcmlwdGlvbiksIGRlZmF1bHRzXVxuICAgICAgLmZpbHRlcihzdHIgPT4gc3RyLmxlbmd0aClcbiAgICAgIC5qb2luKCdcXG4nKTtcbiAgfVxuXG4gIC8qKlxuICAgKiBSZXR1cm5zIGEgdmFsdWUtd2l0aC1kb2N1bWVudGF0aW9uLXN0cmluZyBmb3IgYSBzcGVjaWZpYyBzY2hlbWEgcHJvcGVydHkuXG4gICAqL1xuICBmdW5jdGlvbiBkb2N1bWVudGVkVmFsdWUoXG4gICAgc2NoZW1hOiBJU2V0dGluZ1JlZ2lzdHJ5LklTY2hlbWEsXG4gICAga2V5OiBzdHJpbmcsXG4gICAgdmFsdWU6IEpTT05WYWx1ZVxuICApOiBzdHJpbmcge1xuICAgIGNvbnN0IHByb3BzID0gc2NoZW1hLnByb3BlcnRpZXMgJiYgc2NoZW1hLnByb3BlcnRpZXNba2V5XTtcbiAgICBjb25zdCBkZXNjcmlwdGlvbiA9IChwcm9wcyAmJiBwcm9wc1snZGVzY3JpcHRpb24nXSkgfHwgbm9uZGVzY3JpcHQ7XG4gICAgY29uc3QgdGl0bGUgPSAocHJvcHMgJiYgcHJvcHNbJ3RpdGxlJ10pIHx8IHVudGl0bGVkO1xuICAgIGNvbnN0IHNwYWNlcyA9IGluZGVudC5sZW5ndGg7XG4gICAgY29uc3QgYXR0cmlidXRlID0gcHJlZml4KFxuICAgICAgYFwiJHtrZXl9XCI6ICR7SlNPTi5zdHJpbmdpZnkodmFsdWUsIG51bGwsIHNwYWNlcyl9YCxcbiAgICAgIGluZGVudFxuICAgICk7XG5cbiAgICByZXR1cm4gW3ByZWZpeCh0aXRsZSksIHByZWZpeChkZXNjcmlwdGlvbiksIGF0dHJpYnV0ZV0uam9pbignXFxuJyk7XG4gIH1cblxuICAvKipcbiAgICogUmV0dXJucyBhIGpvaW5lZCBzdHJpbmcgd2l0aCBsaW5lIGJyZWFrcyBhbmQgY29tbWFzIHdoZXJlIGFwcHJvcHJpYXRlLlxuICAgKi9cbiAgZnVuY3Rpb24gam9pbihib2R5OiBzdHJpbmdbXSk6IHN0cmluZyB7XG4gICAgcmV0dXJuIGJvZHkucmVkdWNlKChhY2MsIHZhbCwgaWR4KSA9PiB7XG4gICAgICBjb25zdCByb3dzID0gdmFsLnNwbGl0KCdcXG4nKTtcbiAgICAgIGNvbnN0IGxhc3QgPSByb3dzW3Jvd3MubGVuZ3RoIC0gMV07XG4gICAgICBjb25zdCBjb21tZW50ID0gbGFzdC50cmltKCkuaW5kZXhPZignLy8nKSA9PT0gMDtcbiAgICAgIGNvbnN0IGNvbW1hID0gY29tbWVudCB8fCBpZHggPT09IGJvZHkubGVuZ3RoIC0gMSA/ICcnIDogJywnO1xuICAgICAgY29uc3Qgc2VwYXJhdG9yID0gaWR4ID09PSBib2R5Lmxlbmd0aCAtIDEgPyAnJyA6ICdcXG5cXG4nO1xuXG4gICAgICByZXR1cm4gYWNjICsgdmFsICsgY29tbWEgKyBzZXBhcmF0b3I7XG4gICAgfSwgJycpO1xuICB9XG5cbiAgLyoqXG4gICAqIFJldHVybnMgYSBkb2N1bWVudGF0aW9uIHN0cmluZyB3aXRoIGEgY29tbWVudCBwcmVmaXggYWRkZWQgb24gZXZlcnkgbGluZS5cbiAgICovXG4gIGZ1bmN0aW9uIHByZWZpeChzb3VyY2U6IHN0cmluZywgcHJlID0gYCR7aW5kZW50fS8vIGApOiBzdHJpbmcge1xuICAgIHJldHVybiBwcmUgKyBzb3VyY2Uuc3BsaXQoJ1xcbicpLmpvaW4oYFxcbiR7cHJlfWApO1xuICB9XG5cbiAgLyoqXG4gICAqIENyZWF0ZSBhIGZ1bGx5IGV4dHJhcG9sYXRlZCBkZWZhdWx0IHZhbHVlIGZvciBhIHJvb3Qga2V5IGluIGEgc2NoZW1hLlxuICAgKi9cbiAgZXhwb3J0IGZ1bmN0aW9uIHJlaWZ5RGVmYXVsdChcbiAgICBzY2hlbWE6IElTZXR0aW5nUmVnaXN0cnkuSVByb3BlcnR5LFxuICAgIHJvb3Q/OiBzdHJpbmdcbiAgKTogUGFydGlhbEpTT05WYWx1ZSB8IHVuZGVmaW5lZCB7XG4gICAgLy8gSWYgdGhlIHByb3BlcnR5IGlzIGF0IHRoZSByb290IGxldmVsLCB0cmF2ZXJzZSBpdHMgc2NoZW1hLlxuICAgIHNjaGVtYSA9IChyb290ID8gc2NoZW1hLnByb3BlcnRpZXM/Lltyb290XSA6IHNjaGVtYSkgfHwge307XG5cbiAgICAvLyBJZiB0aGUgcHJvcGVydHkgaGFzIG5vIGRlZmF1bHQgb3IgaXMgYSBwcmltaXRpdmUsIHJldHVybi5cbiAgICBpZiAoISgnZGVmYXVsdCcgaW4gc2NoZW1hKSB8fCBzY2hlbWEudHlwZSAhPT0gJ29iamVjdCcpIHtcbiAgICAgIHJldHVybiBzY2hlbWEuZGVmYXVsdDtcbiAgICB9XG5cbiAgICAvLyBNYWtlIGEgY29weSBvZiB0aGUgZGVmYXVsdCB2YWx1ZSB0byBwb3B1bGF0ZS5cbiAgICBjb25zdCByZXN1bHQgPSBKU09ORXh0LmRlZXBDb3B5KHNjaGVtYS5kZWZhdWx0IGFzIFBhcnRpYWxKU09OT2JqZWN0KTtcblxuICAgIC8vIEl0ZXJhdGUgdGhyb3VnaCBhbmQgcG9wdWxhdGUgZWFjaCBjaGlsZCBwcm9wZXJ0eS5cbiAgICBjb25zdCBwcm9wcyA9IHNjaGVtYS5wcm9wZXJ0aWVzIHx8IHt9O1xuICAgIGZvciAoY29uc3QgcHJvcGVydHkgaW4gcHJvcHMpIHtcbiAgICAgIHJlc3VsdFtwcm9wZXJ0eV0gPSByZWlmeURlZmF1bHQocHJvcHNbcHJvcGVydHldKTtcbiAgICB9XG5cbiAgICByZXR1cm4gcmVzdWx0O1xuICB9XG59XG4iLCIvKiAtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLVxufCBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbnwgRGlzdHJpYnV0ZWQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBNb2RpZmllZCBCU0QgTGljZW5zZS5cbnwtLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKi9cblxuaW1wb3J0IHsgSURhdGFDb25uZWN0b3IgfSBmcm9tICdAanVweXRlcmxhYi9zdGF0ZWRiJztcbmltcG9ydCB7XG4gIFBhcnRpYWxKU09OT2JqZWN0LFxuICBQYXJ0aWFsSlNPTlZhbHVlLFxuICBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0LFxuICBSZWFkb25seVBhcnRpYWxKU09OVmFsdWUsXG4gIFRva2VuXG59IGZyb20gJ0BsdW1pbm8vY29yZXV0aWxzJztcbmltcG9ydCB7IElEaXNwb3NhYmxlIH0gZnJvbSAnQGx1bWluby9kaXNwb3NhYmxlJztcbmltcG9ydCB7IElTaWduYWwgfSBmcm9tICdAbHVtaW5vL3NpZ25hbGluZyc7XG5pbXBvcnQgeyBJU2NoZW1hVmFsaWRhdG9yIH0gZnJvbSAnLi9zZXR0aW5ncmVnaXN0cnknO1xuXG4vKiB0c2xpbnQ6ZGlzYWJsZSAqL1xuLyoqXG4gKiBUaGUgc2V0dGluZyByZWdpc3RyeSB0b2tlbi5cbiAqL1xuZXhwb3J0IGNvbnN0IElTZXR0aW5nUmVnaXN0cnkgPSBuZXcgVG9rZW48SVNldHRpbmdSZWdpc3RyeT4oXG4gICdAanVweXRlcmxhYi9jb3JldXRpbHM6SVNldHRpbmdSZWdpc3RyeSdcbik7XG4vKiB0c2xpbnQ6ZW5hYmxlICovXG5cbi8qKlxuICogVGhlIHNldHRpbmdzIHJlZ2lzdHJ5IGludGVyZmFjZS5cbiAqL1xuZXhwb3J0IGludGVyZmFjZSBJU2V0dGluZ1JlZ2lzdHJ5IHtcbiAgLyoqXG4gICAqIFRoZSBkYXRhIGNvbm5lY3RvciB1c2VkIGJ5IHRoZSBzZXR0aW5nIHJlZ2lzdHJ5LlxuICAgKi9cbiAgcmVhZG9ubHkgY29ubmVjdG9yOiBJRGF0YUNvbm5lY3RvcjxJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW4sIHN0cmluZywgc3RyaW5nPjtcblxuICAvKipcbiAgICogVGhlIHNjaGVtYSBvZiB0aGUgc2V0dGluZyByZWdpc3RyeS5cbiAgICovXG4gIHJlYWRvbmx5IHNjaGVtYTogSVNldHRpbmdSZWdpc3RyeS5JU2NoZW1hO1xuXG4gIC8qKlxuICAgKiBUaGUgc2NoZW1hIHZhbGlkYXRvciB1c2VkIGJ5IHRoZSBzZXR0aW5nIHJlZ2lzdHJ5LlxuICAgKi9cbiAgcmVhZG9ubHkgdmFsaWRhdG9yOiBJU2NoZW1hVmFsaWRhdG9yO1xuXG4gIC8qKlxuICAgKiBBIHNpZ25hbCB0aGF0IGVtaXRzIHRoZSBuYW1lIG9mIGEgcGx1Z2luIHdoZW4gaXRzIHNldHRpbmdzIGNoYW5nZS5cbiAgICovXG4gIHJlYWRvbmx5IHBsdWdpbkNoYW5nZWQ6IElTaWduYWw8dGhpcywgc3RyaW5nPjtcblxuICAvKipcbiAgICogVGhlIGNvbGxlY3Rpb24gb2Ygc2V0dGluZyByZWdpc3RyeSBwbHVnaW5zLlxuICAgKi9cbiAgcmVhZG9ubHkgcGx1Z2luczoge1xuICAgIFtuYW1lOiBzdHJpbmddOiBJU2V0dGluZ1JlZ2lzdHJ5LklQbHVnaW4gfCB1bmRlZmluZWQ7XG4gIH07XG5cbiAgLyoqXG4gICAqIEdldCBhbiBpbmRpdmlkdWFsIHNldHRpbmcuXG4gICAqXG4gICAqIEBwYXJhbSBwbHVnaW4gLSBUaGUgbmFtZSBvZiB0aGUgcGx1Z2luIHdob3NlIHNldHRpbmdzIGFyZSBiZWluZyByZXRyaWV2ZWQuXG4gICAqXG4gICAqIEBwYXJhbSBrZXkgLSBUaGUgbmFtZSBvZiB0aGUgc2V0dGluZyBiZWluZyByZXRyaWV2ZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIHNldHRpbmcgaXMgcmV0cmlldmVkLlxuICAgKi9cbiAgZ2V0KFxuICAgIHBsdWdpbjogc3RyaW5nLFxuICAgIGtleTogc3RyaW5nXG4gICk6IFByb21pc2U8e1xuICAgIGNvbXBvc2l0ZTogUGFydGlhbEpTT05WYWx1ZSB8IHVuZGVmaW5lZDtcbiAgICB1c2VyOiBQYXJ0aWFsSlNPTlZhbHVlIHwgdW5kZWZpbmVkO1xuICB9PjtcblxuICAvKipcbiAgICogTG9hZCBhIHBsdWdpbidzIHNldHRpbmdzIGludG8gdGhlIHNldHRpbmcgcmVnaXN0cnkuXG4gICAqXG4gICAqIEBwYXJhbSBwbHVnaW4gLSBUaGUgbmFtZSBvZiB0aGUgcGx1Z2luIHdob3NlIHNldHRpbmdzIGFyZSBiZWluZyBsb2FkZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdpdGggYSBwbHVnaW4gc2V0dGluZ3Mgb2JqZWN0IG9yIHJlamVjdHNcbiAgICogaWYgdGhlIHBsdWdpbiBpcyBub3QgZm91bmQuXG4gICAqL1xuICBsb2FkKHBsdWdpbjogc3RyaW5nKTogUHJvbWlzZTxJU2V0dGluZ1JlZ2lzdHJ5LklTZXR0aW5ncz47XG5cbiAgLyoqXG4gICAqIFJlbG9hZCBhIHBsdWdpbidzIHNldHRpbmdzIGludG8gdGhlIHJlZ2lzdHJ5IGV2ZW4gaWYgdGhleSBhbHJlYWR5IGV4aXN0LlxuICAgKlxuICAgKiBAcGFyYW0gcGx1Z2luIC0gVGhlIG5hbWUgb2YgdGhlIHBsdWdpbiB3aG9zZSBzZXR0aW5ncyBhcmUgYmVpbmcgcmVsb2FkZWQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdpdGggYSBwbHVnaW4gc2V0dGluZ3Mgb2JqZWN0IG9yIHJlamVjdHNcbiAgICogd2l0aCBhIGxpc3Qgb2YgYElTY2hlbWFWYWxpZGF0b3IuSUVycm9yYCBvYmplY3RzIGlmIGl0IGZhaWxzLlxuICAgKi9cbiAgcmVsb2FkKHBsdWdpbjogc3RyaW5nKTogUHJvbWlzZTxJU2V0dGluZ1JlZ2lzdHJ5LklTZXR0aW5ncz47XG5cbiAgLyoqXG4gICAqIFJlbW92ZSBhIHNpbmdsZSBzZXR0aW5nIGluIHRoZSByZWdpc3RyeS5cbiAgICpcbiAgICogQHBhcmFtIHBsdWdpbiAtIFRoZSBuYW1lIG9mIHRoZSBwbHVnaW4gd2hvc2Ugc2V0dGluZyBpcyBiZWluZyByZW1vdmVkLlxuICAgKlxuICAgKiBAcGFyYW0ga2V5IC0gVGhlIG5hbWUgb2YgdGhlIHNldHRpbmcgYmVpbmcgcmVtb3ZlZC5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2hlbiB0aGUgc2V0dGluZyBpcyByZW1vdmVkLlxuICAgKi9cbiAgcmVtb3ZlKHBsdWdpbjogc3RyaW5nLCBrZXk6IHN0cmluZyk6IFByb21pc2U8dm9pZD47XG5cbiAgLyoqXG4gICAqIFNldCBhIHNpbmdsZSBzZXR0aW5nIGluIHRoZSByZWdpc3RyeS5cbiAgICpcbiAgICogQHBhcmFtIHBsdWdpbiAtIFRoZSBuYW1lIG9mIHRoZSBwbHVnaW4gd2hvc2Ugc2V0dGluZyBpcyBiZWluZyBzZXQuXG4gICAqXG4gICAqIEBwYXJhbSBrZXkgLSBUaGUgbmFtZSBvZiB0aGUgc2V0dGluZyBiZWluZyBzZXQuXG4gICAqXG4gICAqIEBwYXJhbSB2YWx1ZSAtIFRoZSB2YWx1ZSBvZiB0aGUgc2V0dGluZyBiZWluZyBzZXQuXG4gICAqXG4gICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIHNldHRpbmcgaGFzIGJlZW4gc2F2ZWQuXG4gICAqXG4gICAqL1xuICBzZXQocGx1Z2luOiBzdHJpbmcsIGtleTogc3RyaW5nLCB2YWx1ZTogUGFydGlhbEpTT05WYWx1ZSk6IFByb21pc2U8dm9pZD47XG5cbiAgLyoqXG4gICAqIFJlZ2lzdGVyIGEgcGx1Z2luIHRyYW5zZm9ybSBmdW5jdGlvbiB0byBhY3Qgb24gYSBzcGVjaWZpYyBwbHVnaW4uXG4gICAqXG4gICAqIEBwYXJhbSBwbHVnaW4gLSBUaGUgbmFtZSBvZiB0aGUgcGx1Z2luIHdob3NlIHNldHRpbmdzIGFyZSB0cmFuc2Zvcm1lZC5cbiAgICpcbiAgICogQHBhcmFtIHRyYW5zZm9ybXMgLSBUaGUgdHJhbnNmb3JtIGZ1bmN0aW9ucyBhcHBsaWVkIHRvIHRoZSBwbHVnaW4uXG4gICAqXG4gICAqIEByZXR1cm5zIEEgZGlzcG9zYWJsZSB0aGF0IHJlbW92ZXMgdGhlIHRyYW5zZm9ybXMgZnJvbSB0aGUgcmVnaXN0cnkuXG4gICAqXG4gICAqICMjIyMgTm90ZXNcbiAgICogLSBgY29tcG9zZWAgdHJhbnNmb3JtYXRpb25zOiBUaGUgcmVnaXN0cnkgYXV0b21hdGljYWxseSBvdmVyd3JpdGVzIGFcbiAgICogcGx1Z2luJ3MgZGVmYXVsdCB2YWx1ZXMgd2l0aCB1c2VyIG92ZXJyaWRlcywgYnV0IGEgcGx1Z2luIG1heSBpbnN0ZWFkIHdpc2hcbiAgICogdG8gbWVyZ2UgdmFsdWVzLiBUaGlzIGJlaGF2aW9yIGNhbiBiZSBhY2NvbXBsaXNoZWQgaW4gYSBgY29tcG9zZWBcbiAgICogdHJhbnNmb3JtYXRpb24uXG4gICAqIC0gYGZldGNoYCB0cmFuc2Zvcm1hdGlvbnM6IFRoZSByZWdpc3RyeSB1c2VzIHRoZSBwbHVnaW4gZGF0YSB0aGF0IGlzXG4gICAqIGZldGNoZWQgZnJvbSBpdHMgY29ubmVjdG9yLiBJZiBhIHBsdWdpbiB3YW50cyB0byBvdmVycmlkZSwgZS5nLiB0byB1cGRhdGVcbiAgICogaXRzIHNjaGVtYSB3aXRoIGR5bmFtaWMgZGVmYXVsdHMsIGEgYGZldGNoYCB0cmFuc2Zvcm1hdGlvbiBjYW4gYmUgYXBwbGllZC5cbiAgICovXG4gIHRyYW5zZm9ybShcbiAgICBwbHVnaW46IHN0cmluZyxcbiAgICB0cmFuc2Zvcm1zOiB7XG4gICAgICBbcGhhc2UgaW4gSVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luLlBoYXNlXT86IElTZXR0aW5nUmVnaXN0cnkuSVBsdWdpbi5UcmFuc2Zvcm07XG4gICAgfVxuICApOiBJRGlzcG9zYWJsZTtcblxuICAvKipcbiAgICogVXBsb2FkIGEgcGx1Z2luJ3Mgc2V0dGluZ3MuXG4gICAqXG4gICAqIEBwYXJhbSBwbHVnaW4gLSBUaGUgbmFtZSBvZiB0aGUgcGx1Z2luIHdob3NlIHNldHRpbmdzIGFyZSBiZWluZyBzZXQuXG4gICAqXG4gICAqIEBwYXJhbSByYXcgLSBUaGUgcmF3IHBsdWdpbiBzZXR0aW5ncyBiZWluZyB1cGxvYWRlZC5cbiAgICpcbiAgICogQHJldHVybnMgQSBwcm9taXNlIHRoYXQgcmVzb2x2ZXMgd2hlbiB0aGUgc2V0dGluZ3MgaGF2ZSBiZWVuIHNhdmVkLlxuICAgKi9cbiAgdXBsb2FkKHBsdWdpbjogc3RyaW5nLCByYXc6IHN0cmluZyk6IFByb21pc2U8dm9pZD47XG59XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHNldHRpbmcgcmVnaXN0cnkgaW50ZXJmYWNlcy5cbiAqL1xuZXhwb3J0IG5hbWVzcGFjZSBJU2V0dGluZ1JlZ2lzdHJ5IHtcbiAgLyoqXG4gICAqIFRoZSBwcmltaXRpdmUgdHlwZXMgYXZhaWxhYmxlIGluIGEgSlNPTiBzY2hlbWEuXG4gICAqL1xuICBleHBvcnQgdHlwZSBQcmltaXRpdmUgPVxuICAgIHwgJ2FycmF5J1xuICAgIHwgJ2Jvb2xlYW4nXG4gICAgfCAnbnVsbCdcbiAgICB8ICdudW1iZXInXG4gICAgfCAnb2JqZWN0J1xuICAgIHwgJ3N0cmluZyc7XG5cbiAgLyoqXG4gICAqIFRoZSBtZW51IGlkcyBkZWZpbmVkIGJ5IGRlZmF1bHQuXG4gICAqL1xuICBleHBvcnQgdHlwZSBEZWZhdWx0TWVudUlkID1cbiAgICB8ICdqcC1tZW51LWZpbGUnXG4gICAgfCAnanAtbWVudS1maWxlLW5ldydcbiAgICB8ICdqcC1tZW51LWVkaXQnXG4gICAgfCAnanAtbWVudS1oZWxwJ1xuICAgIHwgJ2pwLW1lbnUta2VybmVsJ1xuICAgIHwgJ2pwLW1lbnUtcnVuJ1xuICAgIHwgJ2pwLW1lbnUtc2V0dGluZ3MnXG4gICAgfCAnanAtbWVudS12aWV3J1xuICAgIHwgJ2pwLW1lbnUtdGFicyc7XG5cbiAgLyoqXG4gICAqIE1lbnUgZGVmaW5lZCBieSBhIHNwZWNpZmljIHBsdWdpblxuICAgKi9cbiAgZXhwb3J0IGludGVyZmFjZSBJTWVudSBleHRlbmRzIFBhcnRpYWxKU09OT2JqZWN0IHtcbiAgICAvKipcbiAgICAgKiBVbmlxdWUgbWVudSBpZGVudGlmaWVyXG4gICAgICovXG4gICAgaWQ6IERlZmF1bHRNZW51SWQgfCBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBNZW51IGl0ZW1zXG4gICAgICovXG4gICAgaXRlbXM/OiBJTWVudUl0ZW1bXTtcblxuICAgIC8qKlxuICAgICAqIFRoZSByYW5rIG9yZGVyIG9mIHRoZSBtZW51IGFtb25nIGl0cyBzaWJsaW5ncy5cbiAgICAgKi9cbiAgICByYW5rPzogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogTWVudSB0aXRsZVxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIERlZmF1bHQgd2lsbCBiZSB0aGUgY2FwaXRhbGl6ZWQgaWQuXG4gICAgICovXG4gICAgbGFiZWw/OiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBNZW51IGljb24gaWRcbiAgICAgKlxuICAgICAqICMjIyMgTm90ZVxuICAgICAqIFRoZSBpY29uIGlkIHdpbGwgbG9va2VkIGZvciBpbiByZWdpc3RlcmVkIExhYkljb24uXG4gICAgICovXG4gICAgaWNvbj86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIEdldCB0aGUgbW5lbW9uaWMgaW5kZXggZm9yIHRoZSB0aXRsZS5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBUaGUgZGVmYXVsdCB2YWx1ZSBpcyBgLTFgLlxuICAgICAqL1xuICAgIG1uZW1vbmljPzogbnVtYmVyO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciBhIG1lbnUgaXMgZGlzYWJsZWQuIGBGYWxzZWAgYnkgZGVmYXVsdC5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBUaGlzIGFsbG93cyBhbiB1c2VyIHRvIHN1cHByZXNzIGEgbWVudS5cbiAgICAgKi9cbiAgICBkaXNhYmxlZD86IGJvb2xlYW47XG4gIH1cblxuICBleHBvcnQgaW50ZXJmYWNlIElNZW51SXRlbSBleHRlbmRzIFBhcnRpYWxKU09OT2JqZWN0IHtcbiAgICAvKipcbiAgICAgKiBUaGUgdHlwZSBvZiB0aGUgbWVudSBpdGVtLlxuICAgICAqXG4gICAgICogVGhlIGRlZmF1bHQgdmFsdWUgaXMgYCdjb21tYW5kJ2AuXG4gICAgICovXG4gICAgdHlwZT86ICdjb21tYW5kJyB8ICdzdWJtZW51JyB8ICdzZXBhcmF0b3InO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGNvbW1hbmQgdG8gZXhlY3V0ZSB3aGVuIHRoZSBpdGVtIGlzIHRyaWdnZXJlZC5cbiAgICAgKlxuICAgICAqIFRoZSBkZWZhdWx0IHZhbHVlIGlzIGFuIGVtcHR5IHN0cmluZy5cbiAgICAgKi9cbiAgICBjb21tYW5kPzogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGFyZ3VtZW50cyBmb3IgdGhlIGNvbW1hbmQuXG4gICAgICpcbiAgICAgKiBUaGUgZGVmYXVsdCB2YWx1ZSBpcyBhbiBlbXB0eSBvYmplY3QuXG4gICAgICovXG4gICAgYXJncz86IFBhcnRpYWxKU09OT2JqZWN0O1xuXG4gICAgLyoqXG4gICAgICogVGhlIHJhbmsgb3JkZXIgb2YgdGhlIG1lbnUgaXRlbSBhbW9uZyBpdHMgc2libGluZ3MuXG4gICAgICovXG4gICAgcmFuaz86IG51bWJlcjtcblxuICAgIC8qKlxuICAgICAqIFRoZSBzdWJtZW51IGZvciBhIGAnc3VibWVudSdgIHR5cGUgaXRlbS5cbiAgICAgKlxuICAgICAqIFRoZSBkZWZhdWx0IHZhbHVlIGlzIGBudWxsYC5cbiAgICAgKi9cbiAgICBzdWJtZW51PzogSU1lbnUgfCBudWxsO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciBhIG1lbnUgaXRlbSBpcyBkaXNhYmxlZC4gYGZhbHNlYCBieSBkZWZhdWx0LlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIFRoaXMgYWxsb3dzIGFuIHVzZXIgdG8gc3VwcHJlc3MgbWVudSBpdGVtcy5cbiAgICAgKi9cbiAgICBkaXNhYmxlZD86IGJvb2xlYW47XG4gIH1cblxuICBleHBvcnQgaW50ZXJmYWNlIElDb250ZXh0TWVudUl0ZW0gZXh0ZW5kcyBJTWVudUl0ZW0ge1xuICAgIC8qKlxuICAgICAqIFRoZSBDU1Mgc2VsZWN0b3IgZm9yIHRoZSBjb250ZXh0IG1lbnUgaXRlbS5cbiAgICAgKlxuICAgICAqIFRoZSBjb250ZXh0IG1lbnUgaXRlbSB3aWxsIG9ubHkgYmUgZGlzcGxheWVkIGluIHRoZSBjb250ZXh0IG1lbnVcbiAgICAgKiB3aGVuIHRoZSBzZWxlY3RvciBtYXRjaGVzIGEgbm9kZSBvbiB0aGUgcHJvcGFnYXRpb24gcGF0aCBvZiB0aGVcbiAgICAgKiBjb250ZXh0bWVudSBldmVudC4gVGhpcyBhbGxvd3MgdGhlIG1lbnUgaXRlbSB0byBiZSByZXN0cmljdGVkIHRvXG4gICAgICogdXNlci1kZWZpbmVkIGNvbnRleHRzLlxuICAgICAqXG4gICAgICogVGhlIHNlbGVjdG9yIG11c3Qgbm90IGNvbnRhaW4gY29tbWFzLlxuICAgICAqL1xuICAgIHNlbGVjdG9yOiBzdHJpbmc7XG4gIH1cblxuICAvKipcbiAgICogVGhlIHNldHRpbmdzIGZvciBhIHNwZWNpZmljIHBsdWdpbi5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVBsdWdpbiBleHRlbmRzIFBhcnRpYWxKU09OT2JqZWN0IHtcbiAgICAvKipcbiAgICAgKiBUaGUgbmFtZSBvZiB0aGUgcGx1Z2luLlxuICAgICAqL1xuICAgIGlkOiBzdHJpbmc7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY29sbGVjdGlvbiBvZiB2YWx1ZXMgZm9yIGEgc3BlY2lmaWVkIHBsdWdpbi5cbiAgICAgKi9cbiAgICBkYXRhOiBJU2V0dGluZ0J1bmRsZTtcblxuICAgIC8qKlxuICAgICAqIFRoZSByYXcgdXNlciBzZXR0aW5ncyBkYXRhIGFzIGEgc3RyaW5nIGNvbnRhaW5pbmcgSlNPTiB3aXRoIGNvbW1lbnRzLlxuICAgICAqL1xuICAgIHJhdzogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIEpTT04gc2NoZW1hIGZvciB0aGUgcGx1Z2luLlxuICAgICAqL1xuICAgIHNjaGVtYTogSVNjaGVtYTtcblxuICAgIC8qKlxuICAgICAqIFRoZSBwdWJsaXNoZWQgdmVyc2lvbiBvZiB0aGUgTlBNIHBhY2thZ2UgY29udGFpbmluZyB0aGUgcGx1Z2luLlxuICAgICAqL1xuICAgIHZlcnNpb246IHN0cmluZztcbiAgfVxuXG4gIC8qKlxuICAgKiBBIG5hbWVzcGFjZSBmb3IgcGx1Z2luIGZ1bmN0aW9uYWxpdHkuXG4gICAqL1xuICBleHBvcnQgbmFtZXNwYWNlIElQbHVnaW4ge1xuICAgIC8qKlxuICAgICAqIEEgZnVuY3Rpb24gdGhhdCB0cmFuc2Zvcm1zIGEgcGx1Z2luIG9iamVjdCBiZWZvcmUgaXQgaXMgY29uc3VtZWQgYnkgdGhlXG4gICAgICogc2V0dGluZyByZWdpc3RyeS5cbiAgICAgKi9cbiAgICBleHBvcnQgdHlwZSBUcmFuc2Zvcm0gPSAocGx1Z2luOiBJUGx1Z2luKSA9PiBJUGx1Z2luO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHBoYXNlcyBkdXJpbmcgd2hpY2ggYSB0cmFuc2Zvcm1hdGlvbiBtYXkgYmUgYXBwbGllZCB0byBhIHBsdWdpbi5cbiAgICAgKi9cbiAgICBleHBvcnQgdHlwZSBQaGFzZSA9ICdjb21wb3NlJyB8ICdmZXRjaCc7XG4gIH1cblxuICAvKipcbiAgICogQSBtaW5pbWFsIHN1YnNldCBvZiB0aGUgZm9ybWFsIEpTT04gU2NoZW1hIHRoYXQgZGVzY3JpYmVzIGEgcHJvcGVydHkuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElQcm9wZXJ0eSBleHRlbmRzIFBhcnRpYWxKU09OT2JqZWN0IHtcbiAgICAvKipcbiAgICAgKiBUaGUgZGVmYXVsdCB2YWx1ZSwgaWYgYW55LlxuICAgICAqL1xuICAgIGRlZmF1bHQ/OiBQYXJ0aWFsSlNPTlZhbHVlO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHNjaGVtYSBkZXNjcmlwdGlvbi5cbiAgICAgKi9cbiAgICBkZXNjcmlwdGlvbj86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSBzY2hlbWEncyBjaGlsZCBwcm9wZXJ0aWVzLlxuICAgICAqL1xuICAgIHByb3BlcnRpZXM/OiB7IFtwcm9wZXJ0eTogc3RyaW5nXTogSVByb3BlcnR5IH07XG5cbiAgICAvKipcbiAgICAgKiBUaGUgdGl0bGUgb2YgYSBwcm9wZXJ0eS5cbiAgICAgKi9cbiAgICB0aXRsZT86IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSB0eXBlIG9yIHR5cGVzIG9mIHRoZSBkYXRhLlxuICAgICAqL1xuICAgIHR5cGU/OiBQcmltaXRpdmUgfCBQcmltaXRpdmVbXTtcbiAgfVxuXG4gIC8qKlxuICAgKiBBIHNjaGVtYSB0eXBlIHRoYXQgaXMgYSBtaW5pbWFsIHN1YnNldCBvZiB0aGUgZm9ybWFsIEpTT04gU2NoZW1hIGFsb25nIHdpdGhcbiAgICogb3B0aW9uYWwgSnVweXRlckxhYiByZW5kZXJpbmcgaGludHMuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElTY2hlbWEgZXh0ZW5kcyBJUHJvcGVydHkge1xuICAgIC8qKlxuICAgICAqIFRoZSBKdXB5dGVyTGFiIG1lbnVzIHRoYXQgYXJlIGNyZWF0ZWQgYnkgYSBwbHVnaW4ncyBzY2hlbWEuXG4gICAgICovXG4gICAgJ2p1cHl0ZXIubGFiLm1lbnVzJz86IHtcbiAgICAgIG1haW46IElNZW51W107XG4gICAgICBjb250ZXh0OiBJQ29udGV4dE1lbnVJdGVtW107XG4gICAgfTtcblxuICAgIC8qKlxuICAgICAqIFdoZXRoZXIgdGhlIHNjaGVtYSBpcyBkZXByZWNhdGVkLlxuICAgICAqXG4gICAgICogIyMjIyBOb3Rlc1xuICAgICAqIFRoaXMgZmxhZyBjYW4gYmUgdXNlZCBieSBmdW5jdGlvbmFsaXR5IHRoYXQgbG9hZHMgdGhpcyBwbHVnaW4ncyBzZXR0aW5nc1xuICAgICAqIGZyb20gdGhlIHJlZ2lzdHJ5LiBGb3IgZXhhbXBsZSwgdGhlIHNldHRpbmcgZWRpdG9yIGRvZXMgbm90IGRpc3BsYXkgYVxuICAgICAqIHBsdWdpbidzIHNldHRpbmdzIGlmIGl0IGlzIHNldCB0byBgdHJ1ZWAuXG4gICAgICovXG4gICAgJ2p1cHl0ZXIubGFiLnNldHRpbmctZGVwcmVjYXRlZCc/OiBib29sZWFuO1xuXG4gICAgLyoqXG4gICAgICogVGhlIEp1cHl0ZXJMYWIgaWNvbiBoaW50LlxuICAgICAqL1xuICAgICdqdXB5dGVyLmxhYi5zZXR0aW5nLWljb24nPzogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIEp1cHl0ZXJMYWIgaWNvbiBjbGFzcyBoaW50LlxuICAgICAqL1xuICAgICdqdXB5dGVyLmxhYi5zZXR0aW5nLWljb24tY2xhc3MnPzogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogVGhlIEp1cHl0ZXJMYWIgaWNvbiBsYWJlbCBoaW50LlxuICAgICAqL1xuICAgICdqdXB5dGVyLmxhYi5zZXR0aW5nLWljb24tbGFiZWwnPzogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogQSBmbGFnIHRoYXQgaW5kaWNhdGVzIHBsdWdpbiBzaG91bGQgYmUgdHJhbnNmb3JtZWQgYmVmb3JlIGJlaW5nIHVzZWQgYnlcbiAgICAgKiB0aGUgc2V0dGluZyByZWdpc3RyeS5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBJZiB0aGlzIHZhbHVlIGlzIHNldCB0byBgdHJ1ZWAsIHRoZSBzZXR0aW5nIHJlZ2lzdHJ5IHdpbGwgd2FpdCB1bnRpbCBhXG4gICAgICogdHJhbnNmb3JtYXRpb24gaGFzIGJlZW4gcmVnaXN0ZXJlZCAoYnkgY2FsbGluZyB0aGUgYHRyYW5zZm9ybSgpYCBtZXRob2RcbiAgICAgKiBvZiB0aGUgcmVnaXN0cnkpIGZvciB0aGUgcGx1Z2luIElEIGJlZm9yZSByZXNvbHZpbmcgYGxvYWQoKWAgcHJvbWlzZXMuXG4gICAgICogVGhpcyBtZWFucyB0aGF0IGlmIHRoZSBhdHRyaWJ1dGUgaXMgc2V0IHRvIGB0cnVlYCBidXQgbm8gdHJhbnNmb3JtYXRpb25cbiAgICAgKiBpcyByZWdpc3RlcmVkIGluIHRpbWUsIGNhbGxzIHRvIGBsb2FkKClgIGEgcGx1Z2luIHdpbGwgZXZlbnR1YWxseSB0aW1lXG4gICAgICogb3V0IGFuZCByZWplY3QuXG4gICAgICovXG4gICAgJ2p1cHl0ZXIubGFiLnRyYW5zZm9ybSc/OiBib29sZWFuO1xuXG4gICAgLyoqXG4gICAgICogVGhlIEp1cHl0ZXJMYWIgc2hvcnRjdXRzIHRoYXQgYXJlIGNyZWF0ZWQgYnkgYSBwbHVnaW4ncyBzY2hlbWEuXG4gICAgICovXG4gICAgJ2p1cHl0ZXIubGFiLnNob3J0Y3V0cyc/OiBJU2hvcnRjdXRbXTtcblxuICAgIC8qKlxuICAgICAqIFRoZSByb290IHNjaGVtYSBpcyBhbHdheXMgYW4gb2JqZWN0LlxuICAgICAqL1xuICAgIHR5cGU6ICdvYmplY3QnO1xuICB9XG5cbiAgLyoqXG4gICAqIFRoZSBzZXR0aW5nIHZhbHVlcyBmb3IgYSBwbHVnaW4uXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElTZXR0aW5nQnVuZGxlIGV4dGVuZHMgUGFydGlhbEpTT05PYmplY3Qge1xuICAgIC8qKlxuICAgICAqIEEgY29tcG9zaXRlIG9mIHRoZSB1c2VyIHNldHRpbmcgdmFsdWVzIGFuZCB0aGUgcGx1Z2luIHNjaGVtYSBkZWZhdWx0cy5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBUaGUgYGNvbXBvc2l0ZWAgdmFsdWVzIHdpbGwgYWx3YXlzIGJlIGEgc3VwZXJzZXQgb2YgdGhlIGB1c2VyYCB2YWx1ZXMuXG4gICAgICovXG4gICAgY29tcG9zaXRlOiBQYXJ0aWFsSlNPTk9iamVjdDtcblxuICAgIC8qKlxuICAgICAqIFRoZSB1c2VyIHNldHRpbmcgdmFsdWVzLlxuICAgICAqL1xuICAgIHVzZXI6IFBhcnRpYWxKU09OT2JqZWN0O1xuICB9XG5cbiAgLyoqXG4gICAqIEFuIGludGVyZmFjZSBmb3IgbWFuaXB1bGF0aW5nIHRoZSBzZXR0aW5ncyBvZiBhIHNwZWNpZmljIHBsdWdpbi5cbiAgICovXG4gIGV4cG9ydCBpbnRlcmZhY2UgSVNldHRpbmdzIGV4dGVuZHMgSURpc3Bvc2FibGUge1xuICAgIC8qKlxuICAgICAqIEEgc2lnbmFsIHRoYXQgZW1pdHMgd2hlbiB0aGUgcGx1Z2luJ3Mgc2V0dGluZ3MgaGF2ZSBjaGFuZ2VkLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IGNoYW5nZWQ6IElTaWduYWw8dGhpcywgdm9pZD47XG5cbiAgICAvKipcbiAgICAgKiBUaGUgY29tcG9zaXRlIG9mIHVzZXIgc2V0dGluZ3MgYW5kIGV4dGVuc2lvbiBkZWZhdWx0cy5cbiAgICAgKi9cbiAgICByZWFkb25seSBjb21wb3NpdGU6IFJlYWRvbmx5UGFydGlhbEpTT05PYmplY3Q7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgcGx1Z2luJ3MgSUQuXG4gICAgICovXG4gICAgcmVhZG9ubHkgaWQ6IHN0cmluZztcblxuICAgIC8qXG4gICAgICogVGhlIHVuZGVybHlpbmcgcGx1Z2luLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IHBsdWdpbjogSVNldHRpbmdSZWdpc3RyeS5JUGx1Z2luO1xuXG4gICAgLyoqXG4gICAgICogVGhlIHBsdWdpbiBzZXR0aW5ncyByYXcgdGV4dCB2YWx1ZS5cbiAgICAgKi9cbiAgICByZWFkb25seSByYXc6IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFRoZSBwbHVnaW4ncyBzY2hlbWEuXG4gICAgICovXG4gICAgcmVhZG9ubHkgc2NoZW1hOiBJU2V0dGluZ1JlZ2lzdHJ5LklTY2hlbWE7XG5cbiAgICAvKipcbiAgICAgKiBUaGUgdXNlciBzZXR0aW5ncy5cbiAgICAgKi9cbiAgICByZWFkb25seSB1c2VyOiBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0O1xuXG4gICAgLyoqXG4gICAgICogVGhlIHB1Ymxpc2hlZCB2ZXJzaW9uIG9mIHRoZSBOUE0gcGFja2FnZSBjb250YWluaW5nIHRoZXNlIHNldHRpbmdzLlxuICAgICAqL1xuICAgIHJlYWRvbmx5IHZlcnNpb246IHN0cmluZztcblxuICAgIC8qKlxuICAgICAqIFJldHVybiB0aGUgZGVmYXVsdHMgaW4gYSBjb21tZW50ZWQgSlNPTiBmb3JtYXQuXG4gICAgICovXG4gICAgYW5ub3RhdGVkRGVmYXVsdHMoKTogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogQ2FsY3VsYXRlIHRoZSBkZWZhdWx0IHZhbHVlIG9mIGEgc2V0dGluZyBieSBpdGVyYXRpbmcgdGhyb3VnaCB0aGUgc2NoZW1hLlxuICAgICAqXG4gICAgICogQHBhcmFtIGtleSAtIFRoZSBuYW1lIG9mIHRoZSBzZXR0aW5nIHdob3NlIGRlZmF1bHQgdmFsdWUgaXMgY2FsY3VsYXRlZC5cbiAgICAgKlxuICAgICAqIEByZXR1cm5zIEEgY2FsY3VsYXRlZCBkZWZhdWx0IEpTT04gdmFsdWUgZm9yIGEgc3BlY2lmaWMgc2V0dGluZy5cbiAgICAgKi9cbiAgICBkZWZhdWx0KGtleTogc3RyaW5nKTogUGFydGlhbEpTT05WYWx1ZSB8IHVuZGVmaW5lZDtcblxuICAgIC8qKlxuICAgICAqIEdldCBhbiBpbmRpdmlkdWFsIHNldHRpbmcuXG4gICAgICpcbiAgICAgKiBAcGFyYW0ga2V5IC0gVGhlIG5hbWUgb2YgdGhlIHNldHRpbmcgYmVpbmcgcmV0cmlldmVkLlxuICAgICAqXG4gICAgICogQHJldHVybnMgVGhlIHNldHRpbmcgdmFsdWUuXG4gICAgICovXG4gICAgZ2V0KFxuICAgICAga2V5OiBzdHJpbmdcbiAgICApOiB7XG4gICAgICBjb21wb3NpdGU6IFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZSB8IHVuZGVmaW5lZDtcbiAgICAgIHVzZXI6IFJlYWRvbmx5UGFydGlhbEpTT05WYWx1ZSB8IHVuZGVmaW5lZDtcbiAgICB9O1xuXG4gICAgLyoqXG4gICAgICogUmVtb3ZlIGEgc2luZ2xlIHNldHRpbmcuXG4gICAgICpcbiAgICAgKiBAcGFyYW0ga2V5IC0gVGhlIG5hbWUgb2YgdGhlIHNldHRpbmcgYmVpbmcgcmVtb3ZlZC5cbiAgICAgKlxuICAgICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIHNldHRpbmcgaXMgcmVtb3ZlZC5cbiAgICAgKlxuICAgICAqICMjIyMgTm90ZXNcbiAgICAgKiBUaGlzIGZ1bmN0aW9uIGlzIGFzeW5jaHJvbm91cyBiZWNhdXNlIGl0IHdyaXRlcyB0byB0aGUgc2V0dGluZyByZWdpc3RyeS5cbiAgICAgKi9cbiAgICByZW1vdmUoa2V5OiBzdHJpbmcpOiBQcm9taXNlPHZvaWQ+O1xuXG4gICAgLyoqXG4gICAgICogU2F2ZSBhbGwgb2YgdGhlIHBsdWdpbidzIHVzZXIgc2V0dGluZ3MgYXQgb25jZS5cbiAgICAgKi9cbiAgICBzYXZlKHJhdzogc3RyaW5nKTogUHJvbWlzZTx2b2lkPjtcblxuICAgIC8qKlxuICAgICAqIFNldCBhIHNpbmdsZSBzZXR0aW5nLlxuICAgICAqXG4gICAgICogQHBhcmFtIGtleSAtIFRoZSBuYW1lIG9mIHRoZSBzZXR0aW5nIGJlaW5nIHNldC5cbiAgICAgKlxuICAgICAqIEBwYXJhbSB2YWx1ZSAtIFRoZSB2YWx1ZSBvZiB0aGUgc2V0dGluZy5cbiAgICAgKlxuICAgICAqIEByZXR1cm5zIEEgcHJvbWlzZSB0aGF0IHJlc29sdmVzIHdoZW4gdGhlIHNldHRpbmcgaGFzIGJlZW4gc2F2ZWQuXG4gICAgICpcbiAgICAgKiAjIyMjIE5vdGVzXG4gICAgICogVGhpcyBmdW5jdGlvbiBpcyBhc3luY2hyb25vdXMgYmVjYXVzZSBpdCB3cml0ZXMgdG8gdGhlIHNldHRpbmcgcmVnaXN0cnkuXG4gICAgICovXG4gICAgc2V0KGtleTogc3RyaW5nLCB2YWx1ZTogUGFydGlhbEpTT05WYWx1ZSk6IFByb21pc2U8dm9pZD47XG5cbiAgICAvKipcbiAgICAgKiBWYWxpZGF0ZXMgcmF3IHNldHRpbmdzIHdpdGggY29tbWVudHMuXG4gICAgICpcbiAgICAgKiBAcGFyYW0gcmF3IC0gVGhlIEpTT04gd2l0aCBjb21tZW50cyBzdHJpbmcgYmVpbmcgdmFsaWRhdGVkLlxuICAgICAqXG4gICAgICogQHJldHVybnMgQSBsaXN0IG9mIGVycm9ycyBvciBgbnVsbGAgaWYgdmFsaWQuXG4gICAgICovXG4gICAgdmFsaWRhdGUocmF3OiBzdHJpbmcpOiBJU2NoZW1hVmFsaWRhdG9yLklFcnJvcltdIHwgbnVsbDtcbiAgfVxuXG4gIC8qKlxuICAgKiBBbiBpbnRlcmZhY2UgZGVzY3JpYmluZyBhIEp1cHl0ZXJMYWIga2V5Ym9hcmQgc2hvcnRjdXQuXG4gICAqL1xuICBleHBvcnQgaW50ZXJmYWNlIElTaG9ydGN1dCBleHRlbmRzIFBhcnRpYWxKU09OT2JqZWN0IHtcbiAgICAvKipcbiAgICAgKiBUaGUgb3B0aW9uYWwgYXJndW1lbnRzIHBhc3NlZCBpbnRvIHRoZSBzaG9ydGN1dCdzIGNvbW1hbmQuXG4gICAgICovXG4gICAgYXJncz86IFBhcnRpYWxKU09OT2JqZWN0O1xuXG4gICAgLyoqXG4gICAgICogVGhlIGNvbW1hbmQgaW52b2tlZCBieSB0aGUgc2hvcnRjdXQuXG4gICAgICovXG4gICAgY29tbWFuZDogc3RyaW5nO1xuXG4gICAgLyoqXG4gICAgICogV2hldGhlciBhIGtleWJvYXJkIHNob3J0Y3V0IGlzIGRpc2FibGVkLiBgRmFsc2VgIGJ5IGRlZmF1bHQuXG4gICAgICovXG4gICAgZGlzYWJsZWQ/OiBib29sZWFuO1xuXG4gICAgLyoqXG4gICAgICogVGhlIGtleSBjb21iaW5hdGlvbiBvZiB0aGUgc2hvcnRjdXQuXG4gICAgICovXG4gICAga2V5czogc3RyaW5nW107XG5cbiAgICAvKipcbiAgICAgKiBUaGUgQ1NTIHNlbGVjdG9yIGFwcGxpY2FibGUgdG8gdGhlIHNob3J0Y3V0LlxuICAgICAqL1xuICAgIHNlbGVjdG9yOiBzdHJpbmc7XG4gIH1cbn1cbiJdLCJzb3VyY2VSb290IjoiIn0=