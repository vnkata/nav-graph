/*!
 * autocapture.js v1.0.0-alpha.2.1
 * https://github.com/seeratawan01/autocapture.js#readme
 * Seerat Awan (c) 2022 autocapture.js
 * Released under the MIT License
 */
! function(e, n) {
    "object" == typeof exports && "undefined" != typeof module ? module.exports = n() : "function" == typeof define && define.amd ? define(n) : (e = e || self).getXPath = n()
}(this, function() {
    return function(e) {
        var n = e;
        if (n && n.id) return '//*[@id="' + n.id + '"]';
        for (var o = []; n && Node.ELEMENT_NODE === n.nodeType;) {
            for (var i = 0, r = !1, d = n.previousSibling; d;) d.nodeType !== Node.DOCUMENT_TYPE_NODE && d.nodeName === n.nodeName && i++, d = d.previousSibling;
            for (d = n.nextSibling; d;) {
                if (d.nodeName === n.nodeName) {
                    r = !0;
                    break
                }
                d = d.nextSibling
            }
            o.push((n.prefix ? n.prefix + ":" : "") + n.localName + (i || r ? "[" + (i + 1) + "]" : "")), n = n.parentNode
        }
        return o.length ? "/" + o.reverse().join("/") : ""
    }
});


! function(t, e) {
    "object" == typeof exports && "undefined" != typeof module ? module.exports = e() : "function" == typeof define && define.amd ? define(e) : (t = "undefined" != typeof globalThis ? globalThis : t || self).AutoCapture = e()
}(this, (function() {
    "use strict";

    function t(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r
    }

    function e(e) {
        return function(e) {
            if (Array.isArray(e)) return t(e)
        }(e) || function(t) {
            if ("undefined" != typeof Symbol && null != t[Symbol.iterator] || null != t["@@iterator"]) return Array.from(t)
        }(e) || function(e, n) {
            if (!e) return;
            if ("string" == typeof e) return t(e, n);
            var r = Object.prototype.toString.call(e).slice(8, -1);
            "Object" === r && e.constructor && (r = e.constructor.name);
            if ("Map" === r || "Set" === r) return Array.from(r);
            if ("Arguments" === r || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)) return t(e, n)
        }(e) || function() {
            throw new TypeError("Invalid attempt to spread non-iterable instance.\\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
        }()
    }
    var n = function() {
        function t() {
            ! function(t, e) {
                if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
            }(this, t)
        }
        return t.stringify = function(t) {
            for (var n = arguments.length, r = new Array(n > 1 ? n - 1 : 0), o = 1; o < n; o++) r[o - 1] = arguments[o];
            var i;
            return (i = JSON).stringify.apply(i, [t].concat(e(r)))
        }, t.parse = function(e) {
            var n = JSON.parse(e);
            return "string" == typeof n && (n = t.parse(n)), n
        }, t.isJSON = function(t) {
            try {
                JSON.parse(t)
            } catch (t) {
                return !1
            }
            return !0
        }, t.merge = function() {
            for (var t = arguments.length, e = new Array(t), n = 0; n < t; n++) e[n] = arguments[n];
            for (var r = {}, o = 0; o < e.length; o++) r = Object.assign(r, e[o]);
            return r
        }, t
    }();

    function r(t, e) {
        for (var n = 0; n < e.length; n++) {
            var r = e[n];
            r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(t, r.key, r)
        }
    }
    var o = function() {
            function t() {
                ! function(t, e) {
                    if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
                }(this, t), this.store = {}
            }
            var e, o, i, c = t.prototype;
            return c.setItem = function(t, e) {
                n.isJSON(e) && (e = n.parse(e)), this.store[t] = e
            }, c.getItem = function(t) {
                return this.store[t]
            }, c.removeItem = function(t) {
                delete this.store[t]
            }, c.clear = function() {
                this.store = {}
            }, c.key = function(t) {
                return Object.keys(this.store)[t]
            }, c.getAll = function() {
                return this.store
            }, c.setAll = function(t) {
                this.store = t
            }, c.has = function(t) {
                return this.store.hasOwnProperty(t)
            }, c.size = function() {
                return Object.keys(this.store).length
            }, t.getInstance = function() {
                return t.instance || (t.instance = new t), t.instance
            }, e = t, (o = [{
                key: "length",
                get: function() {
                    return this.size()
                }
            }]) && r(e.prototype, o), i && r(e, i), t
        }(),
        i = {
            ELEMENTS: ["a", "button", "form", "input", "select", "textarea", "label"],
            ATTRIBUTES: ["text", "className", "value", "type", "tagName", "href", "src", "id", "name", "placeholder", "title", "alt", "role"],
            SAFELIST: [],
            CAPTURE: ["tap", "form", "page"],
            PAYLOAD: {},
            PERSISTENCE: "memory",
            STORAGE_KEY: "AUTOCAPTURE_EVENT_DATA",
            VISITOR_ID_KEY: "AUTOCAPTURE_VISITOR_ID",
            MAX_EVENTS: 100,
            MASK_TEXT_CONTENT: !1,
            PLUGINS: ["scroll", "mouse-movement"]
        };

    function c(t, e) {
        for (var n = 0; n < e.length; n++) {
            var r = e[n];
            r.enumerable = r.enumerable || !1, r.configurable = !0, "value" in r && (r.writable = !0), Object.defineProperty(t, r.key, r)
        }
    }
    var u = function() {
        function t(e) {
            if (function(t, e) {
                    if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
                }(this, t), "localStorage" === e || "sessionStorage" === e) this.storage = window[e];
            else if ("memory" === e) this.storage = o.getInstance();
            else {
                if ("none" !== e) throw new Error("Invalid persistence type");
                this.storage = null
            }
        }
        var e, n, r, u = t.prototype;
        return u.setItem = function(t, e) {
            this.storage.setItem(t, e)
        }, u.getItem = function(t) {
            return this.storage.getItem(t)
        }, u.removeItem = function(t) {
            this.storage.removeItem(t)
        }, u.clear = function() {
            this.storage.clear()
        }, u.getAll = function() {
            for (var t = {}, e = 0; e < this.storage.length; e++) {
                var n = this.storage.key(e);
                t[n] = this.getItem(n)
            }
            return t
        }, u.setAll = function(t) {
            for (var e in this.clear(), t) this.setItem(e, t[e])
        }, u.has = function(t) {
            return null !== this.storage.getItem(t)
        }, u.size = function() {
            return this.storage.length
        }, u.key = function(t) {
            return this.storage.key(t)
        }, t.getInstance = function() {
            var e = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : i.PERSISTENCE;
            return t.instance || (t.instance = new t(e)), t.instance.storage
        }, e = t, (n = [{
            key: "length",
            get: function() {
                return this.storage.length
            }
        }]) && c(e.prototype, n), r && c(e, r), t
    }();

    function a(t, e) {
        if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
    }
    u.instance = null;
    var s = function() {
        function t(e, n) {
            var r = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : {},
                o = arguments.length > 3 ? arguments[3] : void 0,
                i = arguments.length > 4 ? arguments[4] : void 0;
            a(this, t), this.key = "dom-event", this.target = document, this.name = e, this.handler = n, this.options = r, this.key = i || this.key, o && (this.target = o)
        }
        var e = t.prototype;
        return e.bind = function() {
            return this.target.addEventListener(this.name, this.handler, this.options), this
        }, e.unbind = function() {
            return this.target.removeEventListener(this.name, this.handler, this.options), this
        }, t
    }();
    var f = function() {
        function t(e) {
            ! function(t, e) {
                if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
            }(this, t), this.settings = {}, this.persistence = null, this.settings = e, this.persistence = u.getInstance(this.settings.persistence || i.PERSISTENCE, this.settings.maxEvents || i.MAX_EVENTS), this.onEventCapture = this.settings.onEventCapture || function(t) {
                return {}
            }
        }
        var e = t.prototype;
        return e.clear = function(t) {
            this.persistence && (t ? this.persistence.removeItem(t) : this.persistence.clear())
        }, e.getAll = function() {
            return this.persistence ? this.persistence.getAll() : {}
        }, t
    }();
    var l = function() {
        function t() {
            ! function(t, e) {
                if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
            }(this, t)
        }
        return t.register = function(e) {
            t.registry.push(e)
        }, t.unregister = function(e) {
            t.registry = t.registry.filter((function(t) {
                return t.key !== e
            }))
        }, t.get = function(e) {
            return t.registry.find((function(t) {
                return t.key === e
            }))
        }, t.getAll = function() {
            return t.registry
        }, t.bind = function(e, n) {
            return t.get(e).bind(n)
        }, t.has = function(e) {
            return !!t.get(e)
        }, t
    }();
    l.registry = [];
    var p = function() {
        function t() {
            ! function(t, e) {
                if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
            }(this, t), this.key = "", this.options = {}
        }
        var e = t.prototype;
        return e.bind = function(t) {
            return []
        }, e.onBeforeCapture = function(t) {
            return !0
        }, e.onEventCapture = function(t) {}, e.onInit = function(t) {
            this.options = t
        }, e.onStart = function() {}, e.onStop = function() {}, e.getOptions = function() {
            return this.options
        }, t
    }();

    function h(t, e) {
        (null == e || e > t.length) && (e = t.length);
        for (var n = 0, r = new Array(e); n < e; n++) r[n] = t[n];
        return r
    }

    function y(t, e) {
        return null != e && "undefined" != typeof Symbol && e[Symbol.hasInstance] ? !!e[Symbol.hasInstance](t) : t instanceof e
    }

    function d(t) {
        return function(t) {
            if (Array.isArray(t)) return h(t)
        }(t) || function(t) {
            if ("undefined" != typeof Symbol && null != t[Symbol.iterator] || null != t["@@iterator"]) return Array.from(t)
        }(t) || function(t, e) {
            if (!t) return;
            if ("string" == typeof t) return h(t, e);
            var n = Object.prototype.toString.call(t).slice(8, -1);
            "Object" === n && t.constructor && (n = t.constructor.name);
            if ("Map" === n || "Set" === n) return Array.from(n);
            if ("Arguments" === n || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return h(t, e)
        }(t) || function() {
            throw new TypeError("Invalid attempt to spread non-iterable instance.\\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
        }()
    }

    function v() {
        return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (function(t) {
            var e = 16 * Math.random() | 0;
            return ("x" == t ? e : 3 & e | 8).toString(16)
        }))
    }

    function g(t, e) {
        var n = e.target.tagName.toLowerCase();
        return -1 !== t.indexOf(n)
    }

    function b(t) {
        return t || function() {
            var t = u.getInstance();
            if (!t) return v();
            var e = t.getItem(i.VISITOR_ID_KEY);
            if (!e) {
                var n = v();
                return t.setItem(i.VISITOR_ID_KEY, n), n
            }
            return e
        }()
    }


function createXPathFromElement(element) { 
  
    if (element.tagName == 'HTML')
        return '/HTML[1]';
    if (element===document.body)
        return '/HTML[1]/BODY[1]';

    var ix= 0;
    var siblings= element.parentNode.childNodes;
    for (var i= 0; i<siblings.length; i++) {
        var sibling= siblings[i];
        if (sibling===element)
            return createXPathFromElement(element.parentNode)+'/'+element.tagName+'['+(ix+1)+']';
        if (sibling.nodeType===1 && sibling.tagName===element.tagName)
            ix++;
    }

}



    function m(t, e) {
        var n = e.attributes,
            r = e.sessionId,
            o = e.payload,
            i = e.type,
            c = e.maskTextContent,
            u = function(t) {
                var e;
                return y(t.target, SVGSVGElement) ? null === (e = t.target) || void 0 === e ? void 0 : e.correspondingUseElement : t.target
            }(t),
            a = {
                event: i || t.type,
                timestamp: (new Date).toISOString(),
                meta: {
                    title: document.title,
                    timestamp: Date.now(),
                    timezone: (new Date).getTimezoneOffset(),
                    url: window.location.href,
                    userAgent: navigator.userAgent,
                    referrer: document.referrer,
                    screen: {
                        width: window.screen.width,
                        height: window.screen.height
                    },
                    window: {
                        width: window.innerWidth,
                        height: window.innerHeight
                    },
                    devicePixelRatio: window.devicePixelRatio,
                    language: navigator.language,
                    platform: navigator.platform,
                    isMobile: /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent),
                    isTouch: "ontouchstart" in window || navigator.maxTouchPoints > 0 || navigator.maxTouchPoints > 0,
                    isBot: /bot|googlebot|crawler|spider|robot|crawling/i.test(navigator.userAgent)
                },
                session: b(r)
            };
        if (o && Object.keys(o).length > 0 && (a.payload = o), u.tagName) {
            var s = u.tagName.toLowerCase();
            a.target = {
                selector: s,
                attributes: {}
            }, n.forEach((function(t) {
                var e = function(t, e, n) {
                    switch (e) {
                        case "text":
                            return getXPath(t);
                            // return function(t, e) {
                            //     var n, r = "";
                            //     return y(t.textContent, SVGAnimatedString) && (r = (null === (n = t.textContent) || void 0 === n ? void 0 : n.baseVal) || ""), r = t.textContent, e && (r = r.replace(/./g, "*")), r
                            // }(t, n);
                        case "className":
                            return y((r = t).className, SVGAnimatedString) ? (null === (o = r.className) || void 0 === o ? void 0 : o.baseVal) || "" : r.className;
                        case "value":
                            return n ? t.value && t.value.length > 0 ? "*****" : "" : t.value;
                        case "type":
                            return t.type;
                        case "tagName":
                            return t.tagName.toLowerCase();
                        case "href":
                            return t.href;
                        case "src":
                            return t.src;
                        case "id":
                            return t.id;
                        case "name":
                            return t.name;
                        case "placeholder":
                            return t.placeholder;
                        case "title":
                            return t.title;
                        case "alt":
                            return t.alt;
                        case "role":
                            return t.getAttribute("role")
                    }
                    var r, o;
                    if (t.hasAttribute(e)) return t.getAttribute(e);
                    return ""
                }(u, t, c);
                e && (a.target.attributes[t] = e)
            }))
        }
        return a
    }

    function w(t, e) {
        var n = arguments.length > 2 && void 0 !== arguments[2] ? arguments[2] : i.MAX_EVENTS;
        if (!e) return !1;
        var r = e.getItem(i.STORAGE_KEY),
            o = r && "string" == typeof r ? JSON.parse(r) : [];
        return o ? (o.length >= n && o.shift(), e.setItem(i.STORAGE_KEY, JSON.stringify(d(o).concat([t]))), !0) : (e.setItem(i.STORAGE_KEY, JSON.stringify([t])), !0)
    }

    function E(t, e, n) {
        return e in t ? Object.defineProperty(t, e, {
            value: n,
            enumerable: !0,
            configurable: !0,
            writable: !0
        }) : t[e] = n, t
    }

    function O(t) {
        return O = Object.setPrototypeOf ? Object.getPrototypeOf : function(t) {
            return t.__proto__ || Object.getPrototypeOf(t)
        }, O(t)
    }

    function S(t, e) {
        return null != e && "undefined" != typeof Symbol && e[Symbol.hasInstance] ? !!e[Symbol.hasInstance](t) : t instanceof e
    }

    function T(t, e) {
        return !e || "object" !== x(e) && "function" != typeof e ? function(t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }(t) : e
    }

    function _(t, e) {
        return _ = Object.setPrototypeOf || function(t, e) {
            return t.__proto__ = e, t
        }, _(t, e)
    }
    var x = function(t) {
        return t && "undefined" != typeof Symbol && t.constructor === Symbol ? "symbol" : typeof t
    };

    function j(t) {
        var e = function() {
            if ("undefined" == typeof Reflect || !Reflect.construct) return !1;
            if (Reflect.construct.sham) return !1;
            if ("function" == typeof Proxy) return !0;
            try {
                return Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], (function() {}))), !0
            } catch (t) {
                return !1
            }
        }();
        return function() {
            var n, r = O(t);
            if (e) {
                var o = O(this).constructor;
                n = Reflect.construct(r, arguments, o)
            } else n = r.apply(this, arguments);
            return T(this, n)
        }
    }
    var P = function(t) {
        ! function(t, e) {
            if ("function" != typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    writable: !0,
                    configurable: !0
                }
            }), e && _(t, e)
        }(r, t);
        var e = j(r);

        function r(t) {
            var n;
            ! function(t, e) {
                if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
            }(this, r);
            var o = Object.assign({}, {
                elements: i.ELEMENTS,
                attributes: i.ATTRIBUTES,
                safelist: i.SAFELIST,
                capture: i.CAPTURE,
                payload: i.PAYLOAD,
                maskTextContent: i.MASK_TEXT_CONTENT,
                sessionId: "",
                persistence: i.PERSISTENCE,
                maxEvents: i.MAX_EVENTS
            }, t);
            return (n = e.call(this, o)).events = [], l.getAll().forEach((function(t) {
                t.onInit(function(t) {
                    for (var e = 1; e < arguments.length; e++) {
                        var n = null != arguments[e] ? arguments[e] : {},
                            r = Object.keys(n);
                        "function" == typeof Object.getOwnPropertySymbols && (r = r.concat(Object.getOwnPropertySymbols(n).filter((function(t) {
                            return Object.getOwnPropertyDescriptor(n, t).enumerable
                        })))), r.forEach((function(e) {
                            E(t, e, n[e])
                        }))
                    }
                    return t
                }({}, o))
            })), n
        }
        var o = r.prototype;
        return o.start = function() {
            this.bind()
        }, o.stop = function() {
            this.unbind(), l.getAll().forEach((function(t) {
                return t.onStop()
            }))
        }, o.startPlugins = function() {
            var t = this;
            l.getAll().forEach((function(e) {
                if (t.settings.capture.includes(e.key)) {
                    var r = e.bind(e.getOptions());
                    if (r) {
                        r.forEach((function(n) {
                            var r = n.target,
                                i = n.event,
                                c = n.callback,
                                u = n.options,
                                a = n.name,
                                f = n.throttle,
                                l = n.condition;
                            (S(r, HTMLElement) || S(r, Document) || S(r, Window)) && "function" == typeof c && "string" == typeof i && t.events.push(new s(i, (function(t) {
                                return o(t, a, c, f, l)
                            }), u, r, e.key).bind())
                        }));
                        var o = function(r, o, i) {
                            var c = arguments.length > 3 && void 0 !== arguments[3] ? arguments[3] : 0,
                                u = arguments.length > 4 ? arguments[4] : void 0;
                            if (!u || "function" != typeof u || u(r)) {
                                if (c) {
                                    var a = Date.now();
                                    if (a - t.lastEvent < c) return;
                                    t.lastEvent = a
                                }
                                if (e.onBeforeCapture(r)) {
                                    var s = m(r, {
                                            attributes: t.settings.attributes,
                                            sessionId: t.settings.sessionId,
                                            payload: t.settings.payload,
                                            type: o,
                                            maskTextContent: t.settings.maskTextContent
                                        }),
                                        f = i(r, s);
                                    if (!1 === f) return;
                                    "object" == typeof f && (s = n.merge(s, {
                                        details: f
                                    })), w(s, t.persistence) && (t.onEventCapture(s), e.onEventCapture(s))
                                }
                            }
                        }
                    }
                }
            }))
        }, o.bind = function() {
            this.startPlugins()
        }, o.unbind = function() {
            this.events.forEach((function(t) {
                return t.unbind()
            }))
        }, o.clearCapturedEvents = function() {
            this.persistence.clear()
        }, o.getCapturedEvents = function() {
            var t, e = null === (t = this.persistence) || void 0 === t ? void 0 : t.getItem(i.STORAGE_KEY);
            return e ? "string" == typeof e ? n.parse(e) : e : []
        }, o.unregisterPlugin = function(t) {
            if (!l.has(t)) throw new Error("The plugin ".concat(t, " is not installed."));
            this.events.filter((function(e) {
                return e.key === t
            })).forEach((function(t) {
                return t.unbind()
            })), l.unregister(t)
        }, r.use = function(t) {
            if (l.get(t.key)) throw new Error("Plugin with key ".concat(t.key, " is already registered."));
            l.register(t)
        }, r
    }(f);

    function R(t, e) {
        if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
    }

    function A(t) {
        return A = Object.setPrototypeOf ? Object.getPrototypeOf : function(t) {
            return t.__proto__ || Object.getPrototypeOf(t)
        }, A(t)
    }

    function I(t, e) {
        return !e || "object" !== C(e) && "function" != typeof e ? function(t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }(t) : e
    }

    function k(t, e) {
        return k = Object.setPrototypeOf || function(t, e) {
            return t.__proto__ = e, t
        }, k(t, e)
    }
    var C = function(t) {
        return t && "undefined" != typeof Symbol && t.constructor === Symbol ? "symbol" : typeof t
    };

    function N(t) {
        var e = function() {
            if ("undefined" == typeof Reflect || !Reflect.construct) return !1;
            if (Reflect.construct.sham) return !1;
            if ("function" == typeof Proxy) return !0;
            try {
                return Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], (function() {}))), !0
            } catch (t) {
                return !1
            }
        }();
        return function() {
            var n, r = A(t);
            if (e) {
                var o = A(this).constructor;
                n = Reflect.construct(r, arguments, o)
            } else n = r.apply(this, arguments);
            return I(this, n)
        }
    }
    var B = function(t) {
        ! function(t, e) {
            if ("function" != typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    writable: !0,
                    configurable: !0
                }
            }), e && k(t, e)
        }(n, t);
        var e = N(n);

        function n() {
            var t;
            return R(this, n), (t = e.apply(this, arguments)).key = "scroll", t.lastScrollTop = 0, t.getScrollDirection = function() {
                var e = window.pageYOffset || document.documentElement.scrollTop;
                return e > t.lastScrollTop ? (t.lastScrollTop = e, "down") : (t.lastScrollTop = e <= 0 ? 0 : e, "up")
            }, t
        }
        var r = n.prototype;
        return r.bind = function(t) {
            var e = this;
            return [{
                name: "scroll",
                target: document,
                event: "scroll",
                callback: function() {
                    return e.captureEvent()
                },
                options: !1
            }]
        }, r.captureEvent = function() {
            return {
                direction: this.getScrollDirection(),
                depth: {
                    x: window.scrollX,
                    y: window.scrollY
                },
                percentage: window.scrollY / (document.body.scrollHeight - window.innerHeight) * 100,
                position: {
                    x: window.scrollX / (document.body.scrollWidth - window.innerWidth),
                    y: window.scrollY / (document.body.scrollHeight - window.innerHeight)
                },
                speed: {
                    x: window.scrollX - window.scrollX,
                    y: window.scrollY - window.scrollY
                },
                size: {
                    x: document.body.scrollWidth - window.innerWidth,
                    y: document.body.scrollHeight - window.innerHeight
                },
                viewport: {
                    x: window.innerWidth,
                    y: window.innerHeight
                }
            }
        }, n
    }(p);

    function D(t, e) {
        if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
    }

    function Y(t) {
        return Y = Object.setPrototypeOf ? Object.getPrototypeOf : function(t) {
            return t.__proto__ || Object.getPrototypeOf(t)
        }, Y(t)
    }

    function M(t, e) {
        return !e || "object" !== X(e) && "function" != typeof e ? function(t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }(t) : e
    }

    function V(t, e) {
        return V = Object.setPrototypeOf || function(t, e) {
            return t.__proto__ = e, t
        }, V(t, e)
    }
    var X = function(t) {
        return t && "undefined" != typeof Symbol && t.constructor === Symbol ? "symbol" : typeof t
    };

    function L(t) {
        var e = function() {
            if ("undefined" == typeof Reflect || !Reflect.construct) return !1;
            if (Reflect.construct.sham) return !1;
            if ("function" == typeof Proxy) return !0;
            try {
                return Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], (function() {}))), !0
            } catch (t) {
                return !1
            }
        }();
        return function() {
            var n, r = Y(t);
            if (e) {
                var o = Y(this).constructor;
                n = Reflect.construct(r, arguments, o)
            } else n = r.apply(this, arguments);
            return M(this, n)
        }
    }
    var U = function(t) {
        ! function(t, e) {
            if ("function" != typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    writable: !0,
                    configurable: !0
                }
            }), e && V(t, e)
        }(n, t);
        var e = L(n);

        function n() {
            var t;
            return D(this, n), (t = e.apply(this, arguments)).key = "page", t
        }
        var r = n.prototype;
        return r.bind = function(t) {
            var e = this;
            return [{
                name: "page",
                target: window,
                event: "load",
                callback: function() {
                    return e.captureEvent("page-load")
                },
                options: {
                    once: !0,
                    capture: !0
                }
            }, {
                name: "page",
                target: window,
                event: "beforeunload",
                callback: function() {
                    return e.captureEvent("page-leave")
                }
            }, {
                name: "page",
                target: window,
                event: "popstate",
                callback: function() {
                    return e.captureEvent("page-change")
                },
                options: {
                    capture: !0
                }
            }]
        }, r.captureEvent = function(t) {
            return {
                type: t
            }
        }, n
    }(p);

    function H(t, e) {
        if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
    }

    function G(t) {
        return G = Object.setPrototypeOf ? Object.getPrototypeOf : function(t) {
            return t.__proto__ || Object.getPrototypeOf(t)
        }, G(t)
    }

    function K(t, e) {
        return !e || "object" !== J(e) && "function" != typeof e ? function(t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }(t) : e
    }

    function W(t, e) {
        return W = Object.setPrototypeOf || function(t, e) {
            return t.__proto__ = e, t
        }, W(t, e)
    }
    var J = function(t) {
        return t && "undefined" != typeof Symbol && t.constructor === Symbol ? "symbol" : typeof t
    };

    function z(t) {
        var e = function() {
            if ("undefined" == typeof Reflect || !Reflect.construct) return !1;
            if (Reflect.construct.sham) return !1;
            if ("function" == typeof Proxy) return !0;
            try {
                return Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], (function() {}))), !0
            } catch (t) {
                return !1
            }
        }();
        return function() {
            var n, r = G(t);
            if (e) {
                var o = G(this).constructor;
                n = Reflect.construct(r, arguments, o)
            } else n = r.apply(this, arguments);
            return K(this, n)
        }
    }
    var F = function(t) {
        ! function(t, e) {
            if ("function" != typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    writable: !0,
                    configurable: !0
                }
            }), e && W(t, e)
        }(n, t);
        var e = z(n);

        function n() {
            var t;
            return H(this, n), (t = e.apply(this, arguments)).key = "mouse-movement", t
        }
        var r = n.prototype;
        return r.bind = function(t) {
            var e = this;
            return [{
                name: "mouse-movement",
                target: document,
                event: "mousemove",
                callback: function(t) {
                    return e.captureEvent(t)
                },
                throttle: 100,
                condition: function() {
                    return !("ontouchstart" in window)
                }
            }]
        }, r.captureEvent = function(t) {
            return {
                x: t.clientX,
                y: t.clientY
            }
        }, n
    }(p);

    function $(t) {
        return $ = Object.setPrototypeOf ? Object.getPrototypeOf : function(t) {
            return t.__proto__ || Object.getPrototypeOf(t)
        }, $(t)
    }

    function q(t, e) {
        return !e || "object" !== Z(e) && "function" != typeof e ? function(t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }(t) : e
    }

    function Q(t, e) {
        return Q = Object.setPrototypeOf || function(t, e) {
            return t.__proto__ = e, t
        }, Q(t, e)
    }
    var Z = function(t) {
        return t && "undefined" != typeof Symbol && t.constructor === Symbol ? "symbol" : typeof t
    };

    function tt(t) {
        var e = function() {
            if ("undefined" == typeof Reflect || !Reflect.construct) return !1;
            if (Reflect.construct.sham) return !1;
            if ("function" == typeof Proxy) return !0;
            try {
                return Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], (function() {}))), !0
            } catch (t) {
                return !1
            }
        }();
        return function() {
            var n, r = $(t);
            if (e) {
                var o = $(this).constructor;
                n = Reflect.construct(r, arguments, o)
            } else n = r.apply(this, arguments);
            return q(this, n)
        }
    }
    var et = function(t) {
        ! function(t, e) {
            if ("function" != typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    writable: !0,
                    configurable: !0
                }
            }), e && Q(t, e)
        }(n, t);
        var e = tt(n);

        function n() {
            var t;
            return function(t, e) {
                if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
            }(this, n), (t = e.call(this)).key = "video", t
        }
        var r = n.prototype;
        return r.bind = function(t) {
            var e = this;
            return [{
                name: "video",
                target: document.getElementsByTagName("video"),
                event: "load",
                callback: function(t) {
                    return e.captureEvent(t)
                }
            }]
        }, r.captureEvent = function(t) {
            var e = t.target;
            return {
                id: e.id,
                state: e.paused ? "pause" : "play",
                duration: e.duration,
                currentTime: e.currentTime,
                percent: e.currentTime / e.duration,
                volume: e.volume,
                muted: e.muted,
                playbackRate: e.playbackRate,
                buffered: e.buffered,
                ended: e.ended,
                paused: e.paused,
                played: e.played,
                readyState: e.readyState,
                seeking: e.seeking,
                src: e.src,
                videoHeight: e.videoHeight,
                videoWidth: e.videoWidth
            }
        }, n
    }(p);

    function nt(t, e) {
        if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
    }

    function rt(t) {
        return rt = Object.setPrototypeOf ? Object.getPrototypeOf : function(t) {
            return t.__proto__ || Object.getPrototypeOf(t)
        }, rt(t)
    }

    function ot(t, e) {
        return !e || "object" !== ct(e) && "function" != typeof e ? function(t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }(t) : e
    }

    function it(t, e) {
        return it = Object.setPrototypeOf || function(t, e) {
            return t.__proto__ = e, t
        }, it(t, e)
    }
    var ct = function(t) {
        return t && "undefined" != typeof Symbol && t.constructor === Symbol ? "symbol" : typeof t
    };

    function ut(t) {
        var e = function() {
            if ("undefined" == typeof Reflect || !Reflect.construct) return !1;
            if (Reflect.construct.sham) return !1;
            if ("function" == typeof Proxy) return !0;
            try {
                return Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], (function() {}))), !0
            } catch (t) {
                return !1
            }
        }();
        return function() {
            var n, r = rt(t);
            if (e) {
                var o = rt(this).constructor;
                n = Reflect.construct(r, arguments, o)
            } else n = r.apply(this, arguments);
            return ot(this, n)
        }
    }
    var at = function(t) {
        ! function(t, e) {
            if ("function" != typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    writable: !0,
                    configurable: !0
                }
            }), e && it(t, e)
        }(n, t);
        var e = ut(n);

        function n() {
            var t;
            return nt(this, n), (t = e.apply(this, arguments)).key = "swipe", t.touchstart = {
                x: 0,
                y: 0
            }, t.touchend = {
                x: 0,
                y: 0
            }, t.fingerCount = 0, t.minDistance = 50, t
        }
        var r = n.prototype;
        return r.bind = function() {
            var t = this;
            return [{
                name: "swipe",
                target: document,
                event: "touchstart",
                callback: function(e) {
                    return t.captureEvent(e)
                }
            }, {
                name: "swipe",
                target: document,
                event: "touchend",
                callback: function(e) {
                    return t.captureEvent(e)
                }
            }]
        }, r.captureEvent = function(t) {
            if ("touchstart" === t.type) return this.touchstart = {
                x: t.touches[0].pageX,
                y: t.touches[0].pageY
            }, this.fingerCount = t.touches.length, !1;
            if ("touchend" === t.type && (this.touchend = {
                    x: t.changedTouches[0].pageX,
                    y: t.changedTouches[0].pageY
                }, this.fingerCount = t.touches.length), 1 === this.fingerCount && 0 !== this.touchend.x) {
                var e = this.touchend.x - this.touchstart.x,
                    n = this.touchend.y - this.touchstart.y,
                    r = Math.sqrt(e * e + n * n),
                    o = this.getDirection(e, n),
                    i = this.getSpeed(r);
                if (r >= this.minDistance) return {
                    direction: o,
                    distance: r,
                    speed: i
                }
            }
            return !1
        }, r.getDirection = function(t, e) {
            return Math.abs(t) > Math.abs(e) ? t > 0 ? "right" : "left" : e > 0 ? "down" : "up"
        }, r.getSpeed = function(t) {
            return t / 100
        }, n
    }(p);

    function st(t, e) {
        if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
    }

    function ft(t, e, n) {
        return e in t ? Object.defineProperty(t, e, {
            value: n,
            enumerable: !0,
            configurable: !0,
            writable: !0
        }) : t[e] = n, t
    }

    function lt(t) {
        return lt = Object.setPrototypeOf ? Object.getPrototypeOf : function(t) {
            return t.__proto__ || Object.getPrototypeOf(t)
        }, lt(t)
    }

    function pt(t, e) {
        return !e || "object" !== yt(e) && "function" != typeof e ? function(t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }(t) : e
    }

    function ht(t, e) {
        return ht = Object.setPrototypeOf || function(t, e) {
            return t.__proto__ = e, t
        }, ht(t, e)
    }
    var yt = function(t) {
        return t && "undefined" != typeof Symbol && t.constructor === Symbol ? "symbol" : typeof t
    };

    function dt(t) {
        var e = function() {
            if ("undefined" == typeof Reflect || !Reflect.construct) return !1;
            if (Reflect.construct.sham) return !1;
            if ("function" == typeof Proxy) return !0;
            try {
                return Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], (function() {}))), !0
            } catch (t) {
                return !1
            }
        }();
        return function() {
            var n, r = lt(t);
            if (e) {
                var o = lt(this).constructor;
                n = Reflect.construct(r, arguments, o)
            } else n = r.apply(this, arguments);
            return pt(this, n)
        }
    }
    var vt = function(t) {
        ! function(t, e) {
            if ("function" != typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    writable: !0,
                    configurable: !0
                }
            }), e && ht(t, e)
        }(n, t);
        var e = dt(n);

        function n() {
            var t;
            return st(this, n), (t = e.apply(this, arguments)).key = "form", t
        }
        var r = n.prototype;
        return r.bind = function(t) {
            var e = this;
            return [{
                name: "form",
                target: document,
                event: "submit",
                callback: function(n) {
                    return e.captureEvent(n, t)
                }
            }, {
                name: "form",
                target: document,
                event: "reset",
                callback: function(n) {
                    return e.captureEvent(n, t)
                }
            }, {
                name: "form",
                target: document,
                event: "input",
                callback: function(n) {
                    return e.captureEvent(n, t)
                }
            }, {
                name: "form",
                target: document,
                event: "change",
                callback: function(n) {
                    return e.captureEvent(n, t)
                }
            }]
        }, r.captureEvent = function(t, e) {
            var n = e.elements,
                r = e.safelist;
            if (!g(n, t)) return !1;
            if (r.some((function(e) {
                    return t.target.matches(e)
                }))) return !1;
            var o, i, c, u, a = t.target,
                s = {};
            a.form && (s = {
                action: null === (o = a.form) || void 0 === o ? void 0 : o.action,
                method: null === (i = a.form) || void 0 === i ? void 0 : i.method,
                id: null === (c = a.form) || void 0 === c ? void 0 : c.id,
                name: null === (u = a.form) || void 0 === u ? void 0 : u.name
            });
            return function(t) {
                for (var e = 1; e < arguments.length; e++) {
                    var n = null != arguments[e] ? arguments[e] : {},
                        r = Object.keys(n);
                    "function" == typeof Object.getOwnPropertySymbols && (r = r.concat(Object.getOwnPropertySymbols(n).filter((function(t) {
                        return Object.getOwnPropertyDescriptor(n, t).enumerable
                    })))), r.forEach((function(e) {
                        ft(t, e, n[e])
                    }))
                }
                return t
            }({
                type: t.type
            }, s)
        }, n
    }(p);

    function gt(t, e) {
        if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
    }

    function bt(t) {
        return bt = Object.setPrototypeOf ? Object.getPrototypeOf : function(t) {
            return t.__proto__ || Object.getPrototypeOf(t)
        }, bt(t)
    }

    function mt(t, e) {
        return !e || "object" !== Et(e) && "function" != typeof e ? function(t) {
            if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
            return t
        }(t) : e
    }

    function wt(t, e) {
        return wt = Object.setPrototypeOf || function(t, e) {
            return t.__proto__ = e, t
        }, wt(t, e)
    }
    var Et = function(t) {
        return t && "undefined" != typeof Symbol && t.constructor === Symbol ? "symbol" : typeof t
    };

    function Ot(t) {
        var e = function() {
            if ("undefined" == typeof Reflect || !Reflect.construct) return !1;
            if (Reflect.construct.sham) return !1;
            if ("function" == typeof Proxy) return !0;
            try {
                return Boolean.prototype.valueOf.call(Reflect.construct(Boolean, [], (function() {}))), !0
            } catch (t) {
                return !1
            }
        }();
        return function() {
            var n, r = bt(t);
            if (e) {
                var o = bt(this).constructor;
                n = Reflect.construct(r, arguments, o)
            } else n = r.apply(this, arguments);
            return mt(this, n)
        }
    }
    var St = function(t) {
        ! function(t, e) {
            if ("function" != typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
            t.prototype = Object.create(e && e.prototype, {
                constructor: {
                    value: t,
                    writable: !0,
                    configurable: !0
                }
            }), e && wt(t, e)
        }(n, t);
        var e = Ot(n);

        function n() {
            var t;
            return gt(this, n), (t = e.apply(this, arguments)).key = "tap", t
        }
        var r = n.prototype;
        return r.bind = function(t) {
            var e = this;
            return [{
                name: "click",
                target: document,
                event: "click",
                callback: function(n) {
                    return e.captureEvent(n, t)
                },
                condition: function() {
                    return !("ontouchstart" in window)
                }
            }, {
                name: "click",
                target: document,
                event: "dblclick",
                callback: function(n) {
                    return e.captureEvent(n, t)
                },
                condition: function() {
                    return !("ontouchstart" in window)
                }
            }, {
                name: "click",
                target: document,
                event: "contextmenu",
                callback: function(n) {
                    return e.captureEvent(n, t)
                }
            }, {
                name: "tap",
                target: document,
                event: "touchstart",
                callback: function(n) {
                    return e.captureEvent(n, t)
                }
            }]
        }, r.captureEvent = function(t, e) {
            var n = e.elements,
                r = e.safelist;
            return !!g(n, t) && (!r.some((function(e) {
                return t.target.matches(e)
            })) && {
                type: "touchstart" === t.type ? "tap" : t.type,
                x: t.clientX,
                y: t.clientY
            })
        }, n
    }(p);
    return P.use(new St), P.use(new vt), P.use(new et), P.use(new at), P.use(new U), P.use(new F), P.use(new B), P
}));
//# sourceMappingURL=autocapture.umd.js.map
