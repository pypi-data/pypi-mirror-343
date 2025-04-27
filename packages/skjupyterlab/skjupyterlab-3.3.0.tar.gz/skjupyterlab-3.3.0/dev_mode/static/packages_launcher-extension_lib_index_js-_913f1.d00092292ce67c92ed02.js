(self["webpackChunk_jupyterlab_application_top"] = self["webpackChunk_jupyterlab_application_top"] || []).push([["packages_launcher-extension_lib_index_js-_913f1"],{

/***/ "../packages/launcher-extension/lib/index.js":
/*!***************************************************!*\
  !*** ../packages/launcher-extension/lib/index.js ***!
  \***************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
/**
 * @packageDocumentation
 * @module launcher-extension
 */






/**
 * The command IDs used by the launcher plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = 'launcher:create';
})(CommandIDs || (CommandIDs = {}));
/**
 * A service providing an interface to the the launcher.
 */
const plugin = {
    activate,
    id: '@jupyterlab/launcher-extension:plugin',
    requires: [_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.ITranslator],
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    provides: _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__.ILauncher,
    autoStart: true
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);
/**
 * Activate the launcher.
 */
function activate(app, translator, labShell, palette) {
    const { commands, shell } = app;
    const trans = translator.load('jupyterlab');
    const model = new _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__.LauncherModel();
    commands.addCommand(CommandIDs.create, {
        label: trans.__('New Launcher'),
        execute: (args) => {
            const cwd = args['cwd'] ? String(args['cwd']) : '';
            const id = `launcher-${Private.id++}`;
            const callback = (item) => {
                shell.add(item, 'main', { ref: id });
            };
            const launcher = new _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__.Launcher({
                model,
                cwd,
                callback,
                commands,
                translator
            });
            launcher.model = model;
            launcher.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.launcherIcon;
            launcher.title.label = trans.__('Launcher');
            const main = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content: launcher });
            // If there are any other widgets open, remove the launcher close icon.
            main.title.closable = !!(0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__.toArray)(shell.widgets('main')).length;
            main.id = id;
            shell.add(main, 'main', { activate: args['activate'] });
            if (labShell) {
                labShell.layoutModified.connect(() => {
                    // If there is only a launcher open, remove the close icon.
                    main.title.closable = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__.toArray)(labShell.widgets('main')).length > 1;
                }, main);
            }
            return main;
        }
    });
    if (palette) {
        palette.addItem({
            command: CommandIDs.create,
            category: trans.__('Launcher')
        });
    }
    return model;
}
/**
 * The namespace for module private data.
 */
var Private;
(function (Private) {
    /**
     * The incrementing id used for launcher widgets.
     */
    Private.id = 0;
})(Private || (Private = {}));


/***/ })

}]);
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9AanVweXRlcmxhYi9hcHBsaWNhdGlvbi10b3AvLi4vcGFja2FnZXMvbGF1bmNoZXItZXh0ZW5zaW9uL3NyYy9pbmRleC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FBQUEsMENBQTBDO0FBQzFDLDJEQUEyRDtBQUMzRDs7O0dBR0c7QUFNOEI7QUFDc0M7QUFDRztBQUNwQjtBQUNHO0FBQ2I7QUFJNUM7O0dBRUc7QUFDSCxJQUFVLFVBQVUsQ0FFbkI7QUFGRCxXQUFVLFVBQVU7SUFDTCxpQkFBTSxHQUFHLGlCQUFpQixDQUFDO0FBQzFDLENBQUMsRUFGUyxVQUFVLEtBQVYsVUFBVSxRQUVuQjtBQUVEOztHQUVHO0FBQ0gsTUFBTSxNQUFNLEdBQXFDO0lBQy9DLFFBQVE7SUFDUixFQUFFLEVBQUUsdUNBQXVDO0lBQzNDLFFBQVEsRUFBRSxDQUFDLGdFQUFXLENBQUM7SUFDdkIsUUFBUSxFQUFFLENBQUMsOERBQVMsRUFBRSxpRUFBZSxDQUFDO0lBQ3RDLFFBQVEsRUFBRSwyREFBUztJQUNuQixTQUFTLEVBQUUsSUFBSTtDQUNoQixDQUFDO0FBRUY7O0dBRUc7QUFDSCxpRUFBZSxNQUFNLEVBQUM7QUFFdEI7O0dBRUc7QUFDSCxTQUFTLFFBQVEsQ0FDZixHQUFvQixFQUNwQixVQUF1QixFQUN2QixRQUEwQixFQUMxQixPQUErQjtJQUUvQixNQUFNLEVBQUUsUUFBUSxFQUFFLEtBQUssRUFBRSxHQUFHLEdBQUcsQ0FBQztJQUNoQyxNQUFNLEtBQUssR0FBRyxVQUFVLENBQUMsSUFBSSxDQUFDLFlBQVksQ0FBQyxDQUFDO0lBQzVDLE1BQU0sS0FBSyxHQUFHLElBQUksK0RBQWEsRUFBRSxDQUFDO0lBRWxDLFFBQVEsQ0FBQyxVQUFVLENBQUMsVUFBVSxDQUFDLE1BQU0sRUFBRTtRQUNyQyxLQUFLLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxjQUFjLENBQUM7UUFDL0IsT0FBTyxFQUFFLENBQUMsSUFBZ0IsRUFBRSxFQUFFO1lBQzVCLE1BQU0sR0FBRyxHQUFHLElBQUksQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDLENBQUMsTUFBTSxDQUFDLElBQUksQ0FBQyxLQUFLLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxFQUFFLENBQUM7WUFDbkQsTUFBTSxFQUFFLEdBQUcsWUFBWSxPQUFPLENBQUMsRUFBRSxFQUFFLEVBQUUsQ0FBQztZQUN0QyxNQUFNLFFBQVEsR0FBRyxDQUFDLElBQVksRUFBRSxFQUFFO2dCQUNoQyxLQUFLLENBQUMsR0FBRyxDQUFDLElBQUksRUFBRSxNQUFNLEVBQUUsRUFBRSxHQUFHLEVBQUUsRUFBRSxFQUFFLENBQUMsQ0FBQztZQUN2QyxDQUFDLENBQUM7WUFDRixNQUFNLFFBQVEsR0FBRyxJQUFJLDBEQUFRLENBQUM7Z0JBQzVCLEtBQUs7Z0JBQ0wsR0FBRztnQkFDSCxRQUFRO2dCQUNSLFFBQVE7Z0JBQ1IsVUFBVTthQUNYLENBQUMsQ0FBQztZQUVILFFBQVEsQ0FBQyxLQUFLLEdBQUcsS0FBSyxDQUFDO1lBQ3ZCLFFBQVEsQ0FBQyxLQUFLLENBQUMsSUFBSSxHQUFHLG1FQUFZLENBQUM7WUFDbkMsUUFBUSxDQUFDLEtBQUssQ0FBQyxLQUFLLEdBQUcsS0FBSyxDQUFDLEVBQUUsQ0FBQyxVQUFVLENBQUMsQ0FBQztZQUU1QyxNQUFNLElBQUksR0FBRyxJQUFJLGdFQUFjLENBQUMsRUFBRSxPQUFPLEVBQUUsUUFBUSxFQUFFLENBQUMsQ0FBQztZQUV2RCx1RUFBdUU7WUFDdkUsSUFBSSxDQUFDLEtBQUssQ0FBQyxRQUFRLEdBQUcsQ0FBQyxDQUFDLDBEQUFPLENBQUMsS0FBSyxDQUFDLE9BQU8sQ0FBQyxNQUFNLENBQUMsQ0FBQyxDQUFDLE1BQU0sQ0FBQztZQUM5RCxJQUFJLENBQUMsRUFBRSxHQUFHLEVBQUUsQ0FBQztZQUViLEtBQUssQ0FBQyxHQUFHLENBQUMsSUFBSSxFQUFFLE1BQU0sRUFBRSxFQUFFLFFBQVEsRUFBRSxJQUFJLENBQUMsVUFBVSxDQUFZLEVBQUUsQ0FBQyxDQUFDO1lBRW5FLElBQUksUUFBUSxFQUFFO2dCQUNaLFFBQVEsQ0FBQyxjQUFjLENBQUMsT0FBTyxDQUFDLEdBQUcsRUFBRTtvQkFDbkMsMkRBQTJEO29CQUMzRCxJQUFJLENBQUMsS0FBSyxDQUFDLFFBQVEsR0FBRywwREFBTyxDQUFDLFFBQVEsQ0FBQyxPQUFPLENBQUMsTUFBTSxDQUFDLENBQUMsQ0FBQyxNQUFNLEdBQUcsQ0FBQyxDQUFDO2dCQUNyRSxDQUFDLEVBQUUsSUFBSSxDQUFDLENBQUM7YUFDVjtZQUVELE9BQU8sSUFBSSxDQUFDO1FBQ2QsQ0FBQztLQUNGLENBQUMsQ0FBQztJQUVILElBQUksT0FBTyxFQUFFO1FBQ1gsT0FBTyxDQUFDLE9BQU8sQ0FBQztZQUNkLE9BQU8sRUFBRSxVQUFVLENBQUMsTUFBTTtZQUMxQixRQUFRLEVBQUUsS0FBSyxDQUFDLEVBQUUsQ0FBQyxVQUFVLENBQUM7U0FDL0IsQ0FBQyxDQUFDO0tBQ0o7SUFFRCxPQUFPLEtBQUssQ0FBQztBQUNmLENBQUM7QUFFRDs7R0FFRztBQUNILElBQVUsT0FBTyxDQUtoQjtBQUxELFdBQVUsT0FBTztJQUNmOztPQUVHO0lBQ1EsVUFBRSxHQUFHLENBQUMsQ0FBQztBQUNwQixDQUFDLEVBTFMsT0FBTyxLQUFQLE9BQU8sUUFLaEIiLCJmaWxlIjoicGFja2FnZXNfbGF1bmNoZXItZXh0ZW5zaW9uX2xpYl9pbmRleF9qcy1fOTEzZjEuZDAwMDkyMjkyY2U2N2M5MmVkMDIuanMiLCJzb3VyY2VzQ29udGVudCI6WyIvLyBDb3B5cmlnaHQgKGMpIEp1cHl0ZXIgRGV2ZWxvcG1lbnQgVGVhbS5cbi8vIERpc3RyaWJ1dGVkIHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgTW9kaWZpZWQgQlNEIExpY2Vuc2UuXG4vKipcbiAqIEBwYWNrYWdlRG9jdW1lbnRhdGlvblxuICogQG1vZHVsZSBsYXVuY2hlci1leHRlbnNpb25cbiAqL1xuXG5pbXBvcnQge1xuICBJTGFiU2hlbGwsXG4gIEp1cHl0ZXJGcm9udEVuZCxcbiAgSnVweXRlckZyb250RW5kUGx1Z2luXG59IGZyb20gJ0BqdXB5dGVybGFiL2FwcGxpY2F0aW9uJztcbmltcG9ydCB7IElDb21tYW5kUGFsZXR0ZSwgTWFpbkFyZWFXaWRnZXQgfSBmcm9tICdAanVweXRlcmxhYi9hcHB1dGlscyc7XG5pbXBvcnQgeyBJTGF1bmNoZXIsIExhdW5jaGVyLCBMYXVuY2hlck1vZGVsIH0gZnJvbSAnQGp1cHl0ZXJsYWIvbGF1bmNoZXInO1xuaW1wb3J0IHsgSVRyYW5zbGF0b3IgfSBmcm9tICdAanVweXRlcmxhYi90cmFuc2xhdGlvbic7XG5pbXBvcnQgeyBsYXVuY2hlckljb24gfSBmcm9tICdAanVweXRlcmxhYi91aS1jb21wb25lbnRzJztcbmltcG9ydCB7IHRvQXJyYXkgfSBmcm9tICdAbHVtaW5vL2FsZ29yaXRobSc7XG5pbXBvcnQgeyBKU09OT2JqZWN0IH0gZnJvbSAnQGx1bWluby9jb3JldXRpbHMnO1xuaW1wb3J0IHsgV2lkZ2V0IH0gZnJvbSAnQGx1bWluby93aWRnZXRzJztcblxuLyoqXG4gKiBUaGUgY29tbWFuZCBJRHMgdXNlZCBieSB0aGUgbGF1bmNoZXIgcGx1Z2luLlxuICovXG5uYW1lc3BhY2UgQ29tbWFuZElEcyB7XG4gIGV4cG9ydCBjb25zdCBjcmVhdGUgPSAnbGF1bmNoZXI6Y3JlYXRlJztcbn1cblxuLyoqXG4gKiBBIHNlcnZpY2UgcHJvdmlkaW5nIGFuIGludGVyZmFjZSB0byB0aGUgdGhlIGxhdW5jaGVyLlxuICovXG5jb25zdCBwbHVnaW46IEp1cHl0ZXJGcm9udEVuZFBsdWdpbjxJTGF1bmNoZXI+ID0ge1xuICBhY3RpdmF0ZSxcbiAgaWQ6ICdAanVweXRlcmxhYi9sYXVuY2hlci1leHRlbnNpb246cGx1Z2luJyxcbiAgcmVxdWlyZXM6IFtJVHJhbnNsYXRvcl0sXG4gIG9wdGlvbmFsOiBbSUxhYlNoZWxsLCBJQ29tbWFuZFBhbGV0dGVdLFxuICBwcm92aWRlczogSUxhdW5jaGVyLFxuICBhdXRvU3RhcnQ6IHRydWVcbn07XG5cbi8qKlxuICogRXhwb3J0IHRoZSBwbHVnaW4gYXMgZGVmYXVsdC5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgcGx1Z2luO1xuXG4vKipcbiAqIEFjdGl2YXRlIHRoZSBsYXVuY2hlci5cbiAqL1xuZnVuY3Rpb24gYWN0aXZhdGUoXG4gIGFwcDogSnVweXRlckZyb250RW5kLFxuICB0cmFuc2xhdG9yOiBJVHJhbnNsYXRvcixcbiAgbGFiU2hlbGw6IElMYWJTaGVsbCB8IG51bGwsXG4gIHBhbGV0dGU6IElDb21tYW5kUGFsZXR0ZSB8IG51bGxcbik6IElMYXVuY2hlciB7XG4gIGNvbnN0IHsgY29tbWFuZHMsIHNoZWxsIH0gPSBhcHA7XG4gIGNvbnN0IHRyYW5zID0gdHJhbnNsYXRvci5sb2FkKCdqdXB5dGVybGFiJyk7XG4gIGNvbnN0IG1vZGVsID0gbmV3IExhdW5jaGVyTW9kZWwoKTtcblxuICBjb21tYW5kcy5hZGRDb21tYW5kKENvbW1hbmRJRHMuY3JlYXRlLCB7XG4gICAgbGFiZWw6IHRyYW5zLl9fKCdOZXcgTGF1bmNoZXInKSxcbiAgICBleGVjdXRlOiAoYXJnczogSlNPTk9iamVjdCkgPT4ge1xuICAgICAgY29uc3QgY3dkID0gYXJnc1snY3dkJ10gPyBTdHJpbmcoYXJnc1snY3dkJ10pIDogJyc7XG4gICAgICBjb25zdCBpZCA9IGBsYXVuY2hlci0ke1ByaXZhdGUuaWQrK31gO1xuICAgICAgY29uc3QgY2FsbGJhY2sgPSAoaXRlbTogV2lkZ2V0KSA9PiB7XG4gICAgICAgIHNoZWxsLmFkZChpdGVtLCAnbWFpbicsIHsgcmVmOiBpZCB9KTtcbiAgICAgIH07XG4gICAgICBjb25zdCBsYXVuY2hlciA9IG5ldyBMYXVuY2hlcih7XG4gICAgICAgIG1vZGVsLFxuICAgICAgICBjd2QsXG4gICAgICAgIGNhbGxiYWNrLFxuICAgICAgICBjb21tYW5kcyxcbiAgICAgICAgdHJhbnNsYXRvclxuICAgICAgfSk7XG5cbiAgICAgIGxhdW5jaGVyLm1vZGVsID0gbW9kZWw7XG4gICAgICBsYXVuY2hlci50aXRsZS5pY29uID0gbGF1bmNoZXJJY29uO1xuICAgICAgbGF1bmNoZXIudGl0bGUubGFiZWwgPSB0cmFucy5fXygnTGF1bmNoZXInKTtcblxuICAgICAgY29uc3QgbWFpbiA9IG5ldyBNYWluQXJlYVdpZGdldCh7IGNvbnRlbnQ6IGxhdW5jaGVyIH0pO1xuXG4gICAgICAvLyBJZiB0aGVyZSBhcmUgYW55IG90aGVyIHdpZGdldHMgb3BlbiwgcmVtb3ZlIHRoZSBsYXVuY2hlciBjbG9zZSBpY29uLlxuICAgICAgbWFpbi50aXRsZS5jbG9zYWJsZSA9ICEhdG9BcnJheShzaGVsbC53aWRnZXRzKCdtYWluJykpLmxlbmd0aDtcbiAgICAgIG1haW4uaWQgPSBpZDtcblxuICAgICAgc2hlbGwuYWRkKG1haW4sICdtYWluJywgeyBhY3RpdmF0ZTogYXJnc1snYWN0aXZhdGUnXSBhcyBib29sZWFuIH0pO1xuXG4gICAgICBpZiAobGFiU2hlbGwpIHtcbiAgICAgICAgbGFiU2hlbGwubGF5b3V0TW9kaWZpZWQuY29ubmVjdCgoKSA9PiB7XG4gICAgICAgICAgLy8gSWYgdGhlcmUgaXMgb25seSBhIGxhdW5jaGVyIG9wZW4sIHJlbW92ZSB0aGUgY2xvc2UgaWNvbi5cbiAgICAgICAgICBtYWluLnRpdGxlLmNsb3NhYmxlID0gdG9BcnJheShsYWJTaGVsbC53aWRnZXRzKCdtYWluJykpLmxlbmd0aCA+IDE7XG4gICAgICAgIH0sIG1haW4pO1xuICAgICAgfVxuXG4gICAgICByZXR1cm4gbWFpbjtcbiAgICB9XG4gIH0pO1xuXG4gIGlmIChwYWxldHRlKSB7XG4gICAgcGFsZXR0ZS5hZGRJdGVtKHtcbiAgICAgIGNvbW1hbmQ6IENvbW1hbmRJRHMuY3JlYXRlLFxuICAgICAgY2F0ZWdvcnk6IHRyYW5zLl9fKCdMYXVuY2hlcicpXG4gICAgfSk7XG4gIH1cblxuICByZXR1cm4gbW9kZWw7XG59XG5cbi8qKlxuICogVGhlIG5hbWVzcGFjZSBmb3IgbW9kdWxlIHByaXZhdGUgZGF0YS5cbiAqL1xubmFtZXNwYWNlIFByaXZhdGUge1xuICAvKipcbiAgICogVGhlIGluY3JlbWVudGluZyBpZCB1c2VkIGZvciBsYXVuY2hlciB3aWRnZXRzLlxuICAgKi9cbiAgZXhwb3J0IGxldCBpZCA9IDA7XG59XG4iXSwic291cmNlUm9vdCI6IiJ9