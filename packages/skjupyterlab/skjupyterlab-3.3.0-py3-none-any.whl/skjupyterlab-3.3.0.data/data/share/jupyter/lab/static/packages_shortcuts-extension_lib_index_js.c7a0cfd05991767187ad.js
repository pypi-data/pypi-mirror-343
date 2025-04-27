(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_shortcuts-extension_lib_index_js"],{

/***/ "../packages/shortcuts-extension/lib/index.js":
/*!****************************************************!*\
  !*** ../packages/shortcuts-extension/lib/index.js ***!
  \****************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_3__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module shortcuts-extension
 */




/**
 * The default shortcuts extension.
 *
 * #### Notes
 * Shortcut values are stored in the setting system. The default values for each
 * shortcut are preset in the settings schema file of this extension.
 * Additionally, each shortcut can be individually set by the end user by
 * modifying its setting (either in the text editor or by modifying its
 * underlying JSON schema file).
 *
 * When setting shortcut selectors, there are two concepts to consider:
 * specificity and matchability. These two interact in sometimes
 * counterintuitive ways. Keyboard events are triggered from an element and
 * they propagate up the DOM until they reach the `documentElement` (`<body>`).
 *
 * When a registered shortcut sequence is fired, the shortcut manager checks
 * the node that fired the event and each of its ancestors until a node matches
 * one or more registered selectors. The *first* matching selector in the
 * chain of ancestors will invoke the shortcut handler and the traversal will
 * end at that point. If a node matches more than one selector, the handler for
 * whichever selector is more *specific* fires.
 * @see https://www.w3.org/TR/css3-selectors/#specificity
 *
 * The practical consequence of this is that a very broadly matching selector,
 * e.g. `'*'` or `'div'` may match and therefore invoke a handler *before* a
 * more specific selector. The most common pitfall is to use the universal
 * (`'*'`) selector. For almost any use case where a global keyboard shortcut is
 * required, using the `'body'` selector is more appropriate.
 */
const shortcuts = {
    id: '@jupyterlab/shortcuts-extension:shortcuts',
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry, _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.ITranslator],
    activate: async (app, registry, translator) => {
        const trans = translator.load('jupyterlab');
        const { commands } = app;
        let canonical;
        let loaded = {};
        /**
         * Populate the plugin's schema defaults.
         */
        function populate(schema) {
            const commands = app.commands.listCommands().join('\n');
            loaded = {};
            schema.properties.shortcuts.default = Object.keys(registry.plugins)
                .map(plugin => {
                const shortcuts = registry.plugins[plugin].schema['jupyter.lab.shortcuts'] || [];
                loaded[plugin] = shortcuts;
                return shortcuts;
            })
                .concat([schema.properties.shortcuts.default])
                .reduce((acc, val) => acc.concat(val), []) // flatten one level
                .sort((a, b) => a.command.localeCompare(b.command));
            schema.properties.shortcuts.description = trans.__(`Note: To disable a system default shortcut,
copy it to User Preferences and add the
"disabled" key, for example:
{
    "command": "application:activate-next-tab",
    "keys": [
        "Ctrl Shift ]"
    ],
    "selector": "body",
    "disabled": true
}

List of commands followed by keyboard shortcuts:
%1

List of keyboard shortcuts:`, commands);
        }
        registry.pluginChanged.connect(async (sender, plugin) => {
            if (plugin !== shortcuts.id) {
                // If the plugin changed its shortcuts, reload everything.
                const oldShortcuts = loaded[plugin];
                const newShortcuts = registry.plugins[plugin].schema['jupyter.lab.shortcuts'] || [];
                if (oldShortcuts === undefined ||
                    !_lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepEqual(oldShortcuts, newShortcuts)) {
                    canonical = null;
                    await registry.reload(shortcuts.id);
                }
            }
        });
        // Transform the plugin object to return different schema than the default.
        registry.transform(shortcuts.id, {
            compose: plugin => {
                var _a, _b, _c, _d;
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                const defaults = (_c = (_b = (_a = canonical.properties) === null || _a === void 0 ? void 0 : _a.shortcuts) === null || _b === void 0 ? void 0 : _b.default) !== null && _c !== void 0 ? _c : [];
                const user = {
                    shortcuts: (_d = plugin.data.user.shortcuts) !== null && _d !== void 0 ? _d : []
                };
                const composite = {
                    shortcuts: _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.SettingRegistry.reconcileShortcuts(defaults, user.shortcuts)
                };
                plugin.data = { composite, user };
                return plugin;
            },
            fetch: plugin => {
                // Only override the canonical schema the first time.
                if (!canonical) {
                    canonical = _lumino_coreutils__WEBPACK_IMPORTED_MODULE_2__.JSONExt.deepCopy(plugin.schema);
                    populate(canonical);
                }
                return {
                    data: plugin.data,
                    id: plugin.id,
                    raw: plugin.raw,
                    schema: canonical,
                    version: plugin.version
                };
            }
        });
        try {
            // Repopulate the canonical variable after the setting registry has
            // preloaded all initial plugins.
            canonical = null;
            const settings = await registry.load(shortcuts.id);
            Private.loadShortcuts(commands, settings.composite);
            settings.changed.connect(() => {
                Private.loadShortcuts(commands, settings.composite);
            });
        }
        catch (error) {
            console.error(`Loading ${shortcuts.id} failed.`, error);
        }
    },
    autoStart: true
};
/**
 * Export the shortcut plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (shortcuts);
/**
 * A namespace for private module data.
 */
var Private;
(function (Private) {
    /**
     * The internal collection of currently loaded shortcuts.
     */
    let disposables;
    /**
     * Load the keyboard shortcuts from settings.
     */
    function loadShortcuts(commands, composite) {
        var _a;
        const shortcuts = ((_a = composite === null || composite === void 0 ? void 0 : composite.shortcuts) !== null && _a !== void 0 ? _a : []);
        if (disposables) {
            disposables.dispose();
        }
        disposables = shortcuts.reduce((acc, val) => {
            const options = normalizeOptions(val);
            if (options) {
                acc.add(commands.addKeyBinding(options));
            }
            return acc;
        }, new _lumino_disposable__WEBPACK_IMPORTED_MODULE_3__.DisposableSet());
    }
    Private.loadShortcuts = loadShortcuts;
    /**
     * Normalize potential keyboard shortcut options.
     */
    function normalizeOptions(value) {
        if (!value || typeof value !== 'object') {
            return undefined;
        }
        const { isArray } = Array;
        const valid = 'command' in value &&
            'keys' in value &&
            'selector' in value &&
            isArray(value.keys);
        return valid ? value : undefined;
    }
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvc2hvcnRjdXRzLWV4dGVuc2lvbi9zcmMvaW5kZXgudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFNNkU7QUFDMUI7QUFNM0I7QUFDcUM7QUFFaEU7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7R0E0Qkc7QUFDSCxNQUFNLFNBQVMsR0FBZ0M7SUFDN0MsRUFBRSxFQUFFLDJDQUEyQztJQUMvQyxRQUFRLEVBQUUsQ0FBQyx5RUFBZ0IsRUFBRSxnRUFBVyxDQUFDO0lBQ3pDLFFBQVEsRUFBRSxLQUFLLEVBQ2IsR0FBb0IsRUFDcEIsUUFBMEIsRUFDMUIsVUFBdUIsRUFDdkIsRUFBRTtRQUNGLE1BQU0sS0FBSyxHQUFHLFVBQVUsQ0FBQyxJQUFJLENBQUMsWUFBWSxDQUFDLENBQUM7UUFDNUMsTUFBTSxFQUFFLFFBQVEsRUFBRSxHQUFHLEdBQUcsQ0FBQztRQUN6QixJQUFJLFNBQTBDLENBQUM7UUFDL0MsSUFBSSxNQUFNLEdBQXFELEVBQUUsQ0FBQztRQUVsRTs7V0FFRztRQUNILFNBQVMsUUFBUSxDQUFDLE1BQWdDO1lBQ2hELE1BQU0sUUFBUSxHQUFHLEdBQUcsQ0FBQyxRQUFRLENBQUMsWUFBWSxFQUFFLENBQUMsSUFBSSxDQUFDLElBQUksQ0FBQyxDQUFDO1lBRXhELE1BQU0sR0FBRyxFQUFFLENBQUM7WUFDWixNQUFNLENBQUMsVUFBVyxDQUFDLFNBQVMsQ0FBQyxPQUFPLEdBQUcsTUFBTSxDQUFDLElBQUksQ0FBQyxRQUFRLENBQUMsT0FBTyxDQUFDO2lCQUNqRSxHQUFHLENBQUMsTUFBTSxDQUFDLEVBQUU7Z0JBQ1osTUFBTSxTQUFTLEdBQ2IsUUFBUSxDQUFDLE9BQU8sQ0FBQyxNQUFNLENBQUUsQ0FBQyxNQUFNLENBQUMsdUJBQXVCLENBQUMs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Q0FBQyxDQUFDLEdBQUcsRUFBRSxHQUFHLEVBQWlCLEVBQUU7WUFDekQsTUFBTSxPQUFPLEdBQUcsZ0JBQWdCLENBQUMsR0FBRyxDQUFDLENBQUM7WUFFdEMsSUFBSSxPQUFPLEVBQUU7Z0JBQ1gsR0FBRyxDQUFDLEdBQUcsQ0FBQyxRQUFRLENBQUMsYUFBYSxDQUFDLE9BQU8sQ0FBQyxDQUFDLENBQUM7YUFDMUM7WUFFRCxPQUFPLEdBQUcsQ0FBQztRQUNiLENBQUMsRUFBRSxJQUFJLDZEQUFhLEVBQUUsQ0FBQyxDQUFDO0lBQzFCLENBQUM7SUFuQmUscUJBQWEsZ0JBbUI1QjtJQUVEOztPQUVHO0lBQ0gsU0FBUyxnQkFBZ0IsQ0FDdkIsS0FFK0M7UUFFL0MsSUFBSSxDQUFDLEtBQUssSUFBSSxPQUFPLEtBQUssS0FBSyxRQUFRLEVBQUU7WUFDdkMsT0FBTyxTQUFTLENBQUM7U0FDbEI7UUFFRCxNQUFNLEVBQUUsT0FBTyxFQUFFLEdBQUcsS0FBSyxDQUFDO1FBQzFCLE1BQU0sS0FBSyxHQUNULFNBQVMsSUFBSSxLQUFLO1lBQ2xCLE1BQU0sSUFBSSxLQUFLO1lBQ2YsVUFBVSxJQUFJLEtBQUs7WUFDbkIsT0FBTyxDQUFFLEtBQXFELENBQUMsSUFBSSxDQUFDLENBQUM7UUFFdkUsT0FBTyxLQUFLLENBQUMsQ0FBQyxDQUFFLEtBQTRDLENBQUMsQ0FBQyxDQUFDLFNBQVMsQ0FBQztJQUMzRSxDQUFDO0FBQ0gsQ0FBQyxFQW5EUyxPQUFPLEtBQVAsT0FBTyxRQW1EaEIiLCJmaWxlIjoicGFja2FnZXNfc2hvcnRjdXRzLWV4dGVuc2lvbl9saWJfaW5kZXhfanMuYzdhMGNmZDA1OTkxNzY3MTg3YWQuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBzaG9ydGN1dHMtZXh0ZW5zaW9uXG4gKi9cblxuaW1wb3J0IHtcbiAgSnVweXRlckZyb250RW5kLFxuICBKdXB5dGVyRnJvbnRFbmRQbHVnaW5cbn0gZnJvbSAnQGp1cHl0ZXJsYWIvYXBwbGljYXRpb24nO1xuaW1wb3J0IHsgSVNldHRpbmdSZWdpc3RyeSwgU2V0dGluZ1JlZ2lzdHJ5IH0gZnJvbSAnQGp1cHl0ZXJsYWIvc2V0dGluZ3JlZ2lzdHJ5JztcbmltcG9ydCB7IElUcmFuc2xhdG9yIH0gZnJvbSAnQGp1cHl0ZXJsYWIvdHJhbnNsYXRpb24nO1xuaW1wb3J0IHsgQ29tbWFuZFJlZ2lzdHJ5IH0gZnJvbSAnQGx1bWluby9jb21tYW5kcyc7XG5pbXBvcnQge1xuICBKU09ORXh0LFxuICBSZWFkb25seVBhcnRpYWxKU09OT2JqZWN0LFxuICBSZWFkb25seVBhcnRpYWxKU09OVmFsdWVcbn0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgRGlzcG9zYWJsZVNldCwgSURpc3Bvc2FibGUgfSBmcm9tICdAbHVtaW5vL2Rpc3Bvc2FibGUnO1xuXG4vKipcbiAqIFRoZSBkZWZhdWx0IHNob3J0Y3V0cyBleHRlbnNpb24uXG4gKlxuICogIyMjIyBOb3Rlc1xuICogU2hvcnRjdXQgdmFsdWVzIGFyZSBzdG9yZWQgaW4gdGhlIHNldHRpbmcgc3lzdGVtLiBUaGUgZGVmYXVsdCB2YWx1ZXMgZm9yIGVhY2hcbiAqIHNob3J0Y3V0IGFyZSBwcmVzZXQgaW4gdGhlIHNldHRpbmdzIHNjaGVtYSBmaWxlIG9mIHRoaXMgZXh0ZW5zaW9uLlxuICogQWRkaXRpb25hbGx5LCBlYWNoIHNob3J0Y3V0IGNhbiBiZSBpbmRpdmlkdWFsbHkgc2V0IGJ5IHRoZSBlbmQgdXNlciBieVxuICogbW9kaWZ5aW5nIGl0cyBzZXR0aW5nIChlaXRoZXIgaW4gdGhlIHRleHQgZWRpdG9yIG9yIGJ5IG1vZGlmeWluZyBpdHNcbiAqIHVuZGVybHlpbmcgSlNPTiBzY2hlbWEgZmlsZSkuXG4gKlxuICogV2hlbiBzZXR0aW5nIHNob3J0Y3V0IHNlbGVjdG9ycywgdGhlcmUgYXJlIHR3byBjb25jZXB0cyB0byBjb25zaWRlcjpcbiAqIHNwZWNpZmljaXR5IGFuZCBtYXRjaGFiaWxpdHkuIFRoZXNlIHR3byBpbnRlcmFjdCBpbiBzb21ldGltZXNcbiAqIGNvdW50ZXJpbnR1aXRpdmUgd2F5cy4gS2V5Ym9hcmQgZXZlbnRzIGFyZSB0cmlnZ2VyZWQgZnJvbSBhbiBlbGVtZW50IGFuZFxuICogdGhleSBwcm9wYWdhdGUgdXAgdGhlIERPTSB1bnRpbCB0aGV5IHJlYWNoIHRoZSBgZG9jdW1lbnRFbGVtZW50YCAoYDxib2R5PmApLlxuICpcbiAqIFdoZW4gYSByZWdpc3RlcmVkIHNob3J0Y3V0IHNlcXVlbmNlIGlzIGZpcmVkLCB0aGUgc2hvcnRjdXQgbWFuYWdlciBjaGVja3NcbiAqIHRoZSBub2RlIHRoYXQgZmlyZWQgdGhlIGV2ZW50IGFuZCBlYWNoIG9mIGl0cyBhbmNlc3RvcnMgdW50aWwgYSBub2RlIG1hdGNoZXNcbiAqIG9uZSBvciBtb3JlIHJlZ2lzdGVyZWQgc2VsZWN0b3JzLiBUaGUgKmZpcnN0KiBtYXRjaGluZyBzZWxlY3RvciBpbiB0aGVcbiAqIGNoYWluIG9mIGFuY2VzdG9ycyB3aWxsIGludm9rZSB0aGUgc2hvcnRjdXQgaGFuZGxlciBhbmQgdGhlIHRyYXZlcnNhbCB3aWxsXG4gKiBlbmQgYXQgdGhhdCBwb2ludC4gSWYgYSBub2RlIG1hdGNoZXMgbW9yZSB0aGFuIG9uZSBzZWxlY3RvciwgdGhlIGhhbmRsZXIgZm9yXG4gKiB3aGljaGV2ZXIgc2VsZWN0b3IgaXMgbW9yZSAqc3BlY2lmaWMqIGZpcmVzLlxuICogQHNlZSBodHRwczovL3d3dy53My5vcmcvVFIvY3NzMy1zZWxlY3RvcnMvI3NwZWNpZmljaXR5XG4gKlxuICogVGhlIHByYWN0aWNhbCBjb25zZXF1ZW5jZSBvZiB0aGlzIGlzIHRoYXQgYSB2ZXJ5IGJyb2FkbHkgbWF0Y2hpbmcgc2VsZWN0b3IsXG4gKiBlLmcuIGAnKidgIG9yIGAnZGl2J2AgbWF5IG1hdGNoIGFuZCB0aGVyZWZvcmUgaW52b2tlIGEgaGFuZGxlciAqYmVmb3JlKiBhXG4gKiBtb3JlIHNwZWNpZmljIHNlbGVjdG9yLiBUaGUgbW9zdCBjb21tb24gcGl0ZmFsbCBpcyB0byB1c2UgdGhlIHVuaXZlcnNhbFxuICogKGAnKidgKSBzZWxlY3Rvci4gRm9yIGFsbW9zdCBhbnkgdXNlIGNhc2Ugd2hlcmUgYSBnbG9iYWwga2V5Ym9hcmQgc2hvcnRjdXQgaXNcbiAqIHJlcXVpcmVkLCB1c2luZyB0aGUgYCdib2R5J2Agc2VsZWN0b3IgaXMgbW9yZSBhcHByb3ByaWF0ZS5cbiAqL1xuY29uc3Qgc2hvcnRjdXRzOiBKdXB5dGVyRnJvbnRFbmRQbHVnaW48dm9pZD4gPSB7XG4gIGlkOiAnQGp1cHl0ZXJsYWIvc2hvcnRjdXRzLWV4dGVuc2lvbjpzaG9ydGN1dHMnLFxuICByZXF1aXJlczogW0lTZXR0aW5nUmVnaXN0cnksIElUcmFuc2xhdG9yXSxcbiAgYWN0aXZhdGU6IGFzeW5jIChcbiAgICBhcHA6IEp1cHl0ZXJGcm9udEVuZCxcbiAgICByZWdpc3RyeTogSVNldHRpbmdSZWdpc3RyeSxcbiAgICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvclxuICApID0+IHtcbiAgICBjb25zdCB0cmFucyA9IHRyYW5zbGF0b3IubG9hZCgnanVweXRlcmxhYicpO1xuICAgIGNvbnN0IHsgY29tbWFuZHMgfSA9IGFwcDtcbiAgICBsZXQgY2Fub25pY2FsOiBJU2V0dGluZ1JlZ2lzdHJ5LklTY2hlbWEgfCBudWxsO1xuICAgIGxldCBsb2FkZWQ6IHsgW25hbWU6IHN0cmluZ106IElTZXR0aW5nUmVnaXN0cnkuSVNob3J0Y3V0W10gfSA9IHt9O1xuXG4gICAgLyoqXG4gICAgICogUG9wdWxhdGUgdGhlIHBsdWdpbidzIHNjaGVtYSBkZWZhdWx0cy5cbiAgICAgKi9cbiAgICBmdW5jdGlvbiBwb3B1bGF0ZShzY2hlbWE6IElTZXR0aW5nUmVnaXN0cnkuSVNjaGVtYSkge1xuICAgICAgY29uc3QgY29tbWFuZHMgPSBhcHAuY29tbWFuZHMubGlzdENvbW1hbmRzKCkuam9pbignXFxuJyk7XG5cbiAgICAgIGxvYWRlZCA9IHt9O1xuICAgICAgc2NoZW1hLnByb3BlcnRpZXMhLnNob3J0Y3V0cy5kZWZhdWx0ID0gT2JqZWN0LmtleXMocmVnaXN0cnkucGx1Z2lucylcbiAgICAgICAgLm1hcChwbHVnaW4gPT4ge1xuICAgICAgICAgIGNvbnN0IHNob3J0Y3V0cyA9XG4gICAgICAgICAgICByZWdpc3RyeS5wbHVnaW5zW3BsdWdpbl0hLnNjaGVtYVsnanVweXRlci5sYWIuc2hvcnRjdXRzJ10gfHwgW107XG4gICAgICAgICAgbG9hZGVkW3BsdWdpbl0gPSBzaG9ydGN1dHM7XG4gICAgICAgICAgcmV0dXJuIHNob3J0Y3V0cztcbiAgICAgICAgfSlcbiAgICAgICAgLmNvbmNhdChbc2NoZW1hLnByb3BlcnRpZXMhLnNob3J0Y3V0cy5kZWZhdWx0IGFzIGFueVtdXSlcbiAgICAgICAgLnJlZHVjZSgoYWNjLCB2YWwpID0+IGFjYy5jb25jYXQodmFsKSwgW10pIC8vIGZsYXR0ZW4gb25lIGxldmVsXG4gICAgICAgIC5zb3J0KChhLCBiKSA9PiBhLmNvbW1hbmQubG9jYWxlQ29tcGFyZShiLmNvbW1hbmQpKTtcblxuICAgICAgc2NoZW1hLnByb3BlcnRpZXMhLnNob3J0Y3V0cy5kZXNjcmlwdGlvbiA9IHRyYW5zLl9fKFxuICAgICAgICBgTm90ZTogVG8gZGlzYWJsZSBhIHN5c3RlbSBkZWZhdWx0IHNob3J0Y3V0LFxuY29weSBpdCB0byBVc2VyIFByZWZlcmVuY2VzIGFuZCBhZGQgdGhlXG5cImRpc2FibGVkXCIga2V5LCBmb3IgZXhhbXBsZTpcbntcbiAgICBcImNvbW1hbmRcIjogXCJhcHBsaWNhdGlvbjphY3RpdmF0ZS1uZXh0LXRhYlwiLFxuICAgIFwia2V5c1wiOiBbXG4gICAgICAgIFwiQ3RybCBTaGlmdCBdXCJcbiAgICBdLFxuICAgIFwic2VsZWN0b3JcIjogXCJib2R5XCIsXG4gICAgXCJkaXNhYmxlZFwiOiB0cnVlXG59XG5cbkxpc3Qgb2YgY29tbWFuZHMgZm9sbG93ZWQgYnkga2V5Ym9hcmQgc2hvcnRjdXRzOlxuJTFcblxuTGlzdCBvZiBrZXlib2FyZCBzaG9ydGN1dHM6YCxcbiAgICAgICAgY29tbWFuZHNcbiAgICAgICk7XG4gICAgfVxuXG4gICAgcmVnaXN0cnkucGx1Z2luQ2hhbmdlZC5jb25uZWN0KGFzeW5jIChzZW5kZXIsIHBsdWdpbikgPT4ge1xuICAgICAgaWYgKHBsdWdpbiAhPT0gc2hvcnRjdXRzLmlkKSB7XG4gICAgICAgIC8vIElmIHRoZSBwbHVnaW4gY2hhbmdlZCBpdHMgc2hvcnRjdXRzLCByZWxvYWQgZXZlcnl0aGluZy5cbiAgICAgICAgY29uc3Qgb2xkU2hvcnRjdXRzID0gbG9hZGVkW3BsdWdpbl07XG4gICAgICAgIGNvbnN0IG5ld1Nob3J0Y3V0cyA9XG4gICAgICAgICAgcmVnaXN0cnkucGx1Z2luc1twbHVnaW5dIS5zY2hlbWFbJ2p1cHl0ZXIubGFiLnNob3J0Y3V0cyddIHx8IFtdO1xuICAgICAgICBpZiAoXG4gICAgICAgICAgb2xkU2hvcnRjdXRzID09PSB1bmRlZmluZWQgfHxcbiAgICAgICAgICAhSlNPTkV4dC5kZWVwRXF1YWwob2xkU2hvcnRjdXRzLCBuZXdTaG9ydGN1dHMpXG4gICAgICAgICkge1xuICAgICAgICAgIGNhbm9uaWNhbCA9IG51bGw7XG4gICAgICAgICAgYXdhaXQgcmVnaXN0cnkucmVsb2FkKHNob3J0Y3V0cy5pZCk7XG4gICAgICAgIH1cbiAgICAgIH1cbiAgICB9KTtcblxuICAgIC8vIFRyYW5zZm9ybSB0aGUgcGx1Z2luIG9iamVjdCB0byByZXR1cm4gZGlmZmVyZW50IHNjaGVtYSB0aGFuIHRoZSBkZWZhdWx0LlxuICAgIHJlZ2lzdHJ5LnRyYW5zZm9ybShzaG9ydGN1dHMuaWQsIHtcbiAgICAgIGNvbXBvc2U6IHBsdWdpbiA9PiB7XG4gICAgICAgIC8vIE9ubHkgb3ZlcnJpZGUgdGhlIGNhbm9uaWNhbCBzY2hlbWEgdGhlIGZpcnN0IHRpbWUuXG4gICAgICAgIGlmICghY2Fub25pY2FsKSB7XG4gICAgICAgICAgY2Fub25pY2FsID0gSlNPTkV4dC5kZWVwQ29weShwbHVnaW4uc2NoZW1hKTtcbiAgICAgICAgICBwb3B1bGF0ZShjYW5vbmljYWwpO1xuICAgICAgICB9XG5cbiAgICAgICAgY29uc3QgZGVmYXVsdHMgPSBjYW5vbmljYWwucHJvcGVydGllcz8uc2hvcnRjdXRzPy5kZWZhdWx0ID8/IFtdO1xuICAgICAgICBjb25zdCB1c2VyID0ge1xuICAgICAgICAgIHNob3J0Y3V0czogcGx1Z2luLmRhdGEudXNlci5zaG9ydGN1dHMgPz8gW11cbiAgICAgICAgfTtcbiAgICAgICAgY29uc3QgY29tcG9zaXRlID0ge1xuICAgICAgICAgIHNob3J0Y3V0czogU2V0dGluZ1JlZ2lzdHJ5LnJlY29uY2lsZVNob3J0Y3V0cyhcbiAgICAgICAgICAgIGRlZmF1bHRzIGFzIElTZXR0aW5nUmVnaXN0cnkuSVNob3J0Y3V0W10sXG4gICAgICAgICAgICB1c2VyLnNob3J0Y3V0cyBhcyBJU2V0dGluZ1JlZ2lzdHJ5LklTaG9ydGN1dFtdXG4gICAgICAgICAgKVxuICAgICAgICB9O1xuXG4gICAgICAgIHBsdWdpbi5kYXRhID0geyBjb21wb3NpdGUsIHVzZXIgfTtcblxuICAgICAgICByZXR1cm4gcGx1Z2luO1xuICAgICAgfSxcbiAgICAgIGZldGNoOiBwbHVnaW4gPT4ge1xuICAgICAgICAvLyBPbmx5IG92ZXJyaWRlIHRoZSBjYW5vbmljYWwgc2NoZW1hIHRoZSBmaXJzdCB0aW1lLlxuICAgICAgICBpZiAoIWNhbm9uaWNhbCkge1xuICAgICAgICAgIGNhbm9uaWNhbCA9IEpTT05FeHQuZGVlcENvcHkocGx1Z2luLnNjaGVtYSk7XG4gICAgICAgICAgcG9wdWxhdGUoY2Fub25pY2FsKTtcbiAgICAgICAgfVxuXG4gICAgICAgIHJldHVybiB7XG4gICAgICAgICAgZGF0YTogcGx1Z2luLmRhdGEsXG4gICAgICAgICAgaWQ6IHBsdWdpbi5pZCxcbiAgICAgICAgICByYXc6IHBsdWdpbi5yYXcsXG4gICAgICAgICAgc2NoZW1hOiBjYW5vbmljYWwsXG4gICAgICAgICAgdmVyc2lvbjogcGx1Z2luLnZlcnNpb25cbiAgICAgICAgfTtcbiAgICAgIH1cbiAgICB9KTtcblxuICAgIHRyeSB7XG4gICAgICAvLyBSZXBvcHVsYXRlIHRoZSBjYW5vbmljYWwgdmFyaWFibGUgYWZ0ZXIgdGhlIHNldHRpbmcgcmVnaXN0cnkgaGFzXG4gICAgICAvLyBwcmVsb2FkZWQgYWxsIGluaXRpYWwgcGx1Z2lucy5cbiAgICAgIGNhbm9uaWNhbCA9IG51bGw7XG5cbiAgICAgIGNvbnN0IHNldHRpbmdzID0gYXdhaXQgcmVnaXN0cnkubG9hZChzaG9ydGN1dHMuaWQpO1xuXG4gICAgICBQcml2YXRlLmxvYWRTaG9ydGN1dHMoY29tbWFuZHMsIHNldHRpbmdzLmNvbXBvc2l0ZSk7XG4gICAgICBzZXR0aW5ncy5jaGFuZ2VkLmNvbm5lY3QoKCkgPT4ge1xuICAgICAgICBQcml2YXRlLmxvYWRTaG9ydGN1dHMoY29tbWFuZHMsIHNldHRpbmdzLmNvbXBvc2l0ZSk7XG4gICAgICB9KTtcbiAgICB9IGNhdGNoIChlcnJvcikge1xuICAgICAgY29uc29sZS5lcnJvcihgTG9hZGluZyAke3Nob3J0Y3V0cy5pZH0gZmFpbGVkLmAsIGVycm9yKTtcbiAgICB9XG4gIH0sXG4gIGF1dG9TdGFydDogdHJ1ZVxufTtcblxuLyoqXG4gKiBFeHBvcnQgdGhlIHNob3J0Y3V0IHBsdWdpbiBhcyBkZWZhdWx0LlxuICovXG5leHBvcnQgZGVmYXVsdCBzaG9ydGN1dHM7XG5cbi8qKlxuICogQSBuYW1lc3BhY2UgZm9yIHByaXZhdGUgbW9kdWxlIGRhdGEuXG4gKi9cbm5hbWVzcGFjZSBQcml2YXRlIHtcbiAgLyoqXG4gICAqIFRoZSBpbnRlcm5hbCBjb2xsZWN0aW9uIG9mIGN1cnJlbnRseSBsb2FkZWQgc2hvcnRjdXRzLlxuICAgKi9cbiAgbGV0IGRpc3Bvc2FibGVzOiBJRGlzcG9zYWJsZTtcblxuICAvKipcbiAgICogTG9hZCB0aGUga2V5Ym9hcmQgc2hvcnRjdXRzIGZyb20gc2V0dGluZ3MuXG4gICAqL1xuICBleHBvcnQgZnVuY3Rpb24gbG9hZFNob3J0Y3V0cyhcbiAgICBjb21tYW5kczogQ29tbWFuZFJlZ2lzdHJ5LFxuICAgIGNvbXBvc2l0ZTogUmVhZG9ubHlQYXJ0aWFsSlNPTk9iamVjdCB8IHVuZGVmaW5lZFxuICApOiB2b2lkIHtcbiAgICBjb25zdCBzaG9ydGN1dHMgPSAoY29tcG9zaXRlPy5zaG9ydGN1dHMgPz9cbiAgICAgIFtdKSBhcyBJU2V0dGluZ1JlZ2lzdHJ5LklTaG9ydGN1dFtdO1xuXG4gICAgaWYgKGRpc3Bvc2FibGVzKSB7XG4gICAgICBkaXNwb3NhYmxlcy5kaXNwb3NlKCk7XG4gICAgfVxuICAgIGRpc3Bvc2FibGVzID0gc2hvcnRjdXRzLnJlZHVjZSgoYWNjLCB2YWwpOiBEaXNwb3NhYmxlU2V0ID0+IHtcbiAgICAgIGNvbnN0IG9wdGlvbnMgPSBub3JtYWxpemVPcHRpb25zKHZhbCk7XG5cbiAgICAgIGlmIChvcHRpb25zKSB7XG4gICAgICAgIGFjYy5hZGQoY29tbWFuZHMuYWRkS2V5QmluZGluZyhvcHRpb25zKSk7XG4gICAgICB9XG5cbiAgICAgIHJldHVybiBhY2M7XG4gICAgfSwgbmV3IERpc3Bvc2FibGVTZXQoKSk7XG4gIH1cblxuICAvKipcbiAgICogTm9ybWFsaXplIHBvdGVudGlhbCBrZXlib2FyZCBzaG9ydGN1dCBvcHRpb25zLlxuICAgKi9cbiAgZnVuY3Rpb24gbm9ybWFsaXplT3B0aW9ucyhcbiAgICB2YWx1ZTpcbiAgICAgIHwgUmVhZG9ubHlQYXJ0aWFsSlNPTlZhbHVlXG4gICAgICB8IFBhcnRpYWw8Q29tbWFuZFJlZ2lzdHJ5LklLZXlCaW5kaW5nT3B0aW9ucz5cbiAgKTogQ29tbWFuZFJlZ2lzdHJ5LklLZXlCaW5kaW5nT3B0aW9ucyB8IHVuZGVmaW5lZCB7XG4gICAgaWYgKCF2YWx1ZSB8fCB0eXBlb2YgdmFsdWUgIT09ICdvYmplY3QnKSB7XG4gICAgICByZXR1cm4gdW5kZWZpbmVkO1xuICAgIH1cblxuICAgIGNvbnN0IHsgaXNBcnJheSB9ID0gQXJyYXk7XG4gICAgY29uc3QgdmFsaWQgPVxuICAgICAgJ2NvbW1hbmQnIGluIHZhbHVlICYmXG4gICAgICAna2V5cycgaW4gdmFsdWUgJiZcbiAgICAgICdzZWxlY3RvcicgaW4gdmFsdWUgJiZcbiAgICAgIGlzQXJyYXkoKHZhbHVlIGFzIFBhcnRpYWw8Q29tbWFuZFJlZ2lzdHJ5LklLZXlCaW5kaW5nT3B0aW9ucz4pLmtleXMpO1xuXG4gICAgcmV0dXJuIHZhbGlkID8gKHZhbHVlIGFzIENvbW1hbmRSZWdpc3RyeS5JS2V5QmluZGluZ09wdGlvbnMpIDogdW5kZWZpbmVkO1xuICB9XG59XG4iXSwic291cmNlUm9vdCI6IiJ9