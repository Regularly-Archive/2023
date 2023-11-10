var Dry = (function () {
  'use strict';

  function _classCallCheck(instance, Constructor) {
    if (!(instance instanceof Constructor)) {
      throw new TypeError("Cannot call a class as a function");
    }
  }
  function _defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];
      descriptor.enumerable = descriptor.enumerable || false;
      descriptor.configurable = true;
      if ("value" in descriptor) descriptor.writable = true;
      Object.defineProperty(target, _toPropertyKey(descriptor.key), descriptor);
    }
  }
  function _createClass(Constructor, protoProps, staticProps) {
    if (protoProps) _defineProperties(Constructor.prototype, protoProps);
    if (staticProps) _defineProperties(Constructor, staticProps);
    Object.defineProperty(Constructor, "prototype", {
      writable: false
    });
    return Constructor;
  }
  function _defineProperty(obj, key, value) {
    key = _toPropertyKey(key);
    if (key in obj) {
      Object.defineProperty(obj, key, {
        value: value,
        enumerable: true,
        configurable: true,
        writable: true
      });
    } else {
      obj[key] = value;
    }
    return obj;
  }
  function _unsupportedIterableToArray(o, minLen) {
    if (!o) return;
    if (typeof o === "string") return _arrayLikeToArray(o, minLen);
    var n = Object.prototype.toString.call(o).slice(8, -1);
    if (n === "Object" && o.constructor) n = o.constructor.name;
    if (n === "Map" || n === "Set") return Array.from(o);
    if (n === "Arguments" || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)) return _arrayLikeToArray(o, minLen);
  }
  function _arrayLikeToArray(arr, len) {
    if (len == null || len > arr.length) len = arr.length;
    for (var i = 0, arr2 = new Array(len); i < len; i++) arr2[i] = arr[i];
    return arr2;
  }
  function _createForOfIteratorHelper(o, allowArrayLike) {
    var it = typeof Symbol !== "undefined" && o[Symbol.iterator] || o["@@iterator"];
    if (!it) {
      if (Array.isArray(o) || (it = _unsupportedIterableToArray(o)) || allowArrayLike && o && typeof o.length === "number") {
        if (it) o = it;
        var i = 0;
        var F = function () {};
        return {
          s: F,
          n: function () {
            if (i >= o.length) return {
              done: true
            };
            return {
              done: false,
              value: o[i++]
            };
          },
          e: function (e) {
            throw e;
          },
          f: F
        };
      }
      throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.");
    }
    var normalCompletion = true,
      didErr = false,
      err;
    return {
      s: function () {
        it = it.call(o);
      },
      n: function () {
        var step = it.next();
        normalCompletion = step.done;
        return step;
      },
      e: function (e) {
        didErr = true;
        err = e;
      },
      f: function () {
        try {
          if (!normalCompletion && it.return != null) it.return();
        } finally {
          if (didErr) throw err;
        }
      }
    };
  }
  function _toPrimitive(input, hint) {
    if (typeof input !== "object" || input === null) return input;
    var prim = input[Symbol.toPrimitive];
    if (prim !== undefined) {
      var res = prim.call(input, hint || "default");
      if (typeof res !== "object") return res;
      throw new TypeError("@@toPrimitive must return a primitive value.");
    }
    return (hint === "string" ? String : Number)(input);
  }
  function _toPropertyKey(arg) {
    var key = _toPrimitive(arg, "string");
    return typeof key === "symbol" ? key : String(key);
  }

  var HTTPS_BASE_URL = 'https://speech.platform.bing.com/consumer/speech/synthesize';
  var TRUSTED_CLIENT_TOKEN = "6A5AA1D4EAFF4E9FB37E23D68491D6F4";
  var VOICE_LIST = "".concat(HTTPS_BASE_URL, "/readaloud/voices/list?trustedclienttoken=").concat(TRUSTED_CLIENT_TOKEN);

  var list_voices = function list_voices() {
    var data = fetch(VOICE_LIST, {
      mode: "cors",
      method: 'GET',
      credentials: 'include',
      headers: {
        "Authority": "speech.platform.bing.com",
        "Sec-CH-UA": '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
        "Sec-CH-UA-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41",
        "Accept": "*/*",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9"
      }
    }).then(function (res) {
      return res.json();
    })["catch"](function (error) {
      return console.error(error);
    });
    return data;
  };
  var VoicesManager = /*#__PURE__*/function () {
    function VoicesManager() {
      _classCallCheck(this, VoicesManager);
    }
    _createClass(VoicesManager, null, [{
      key: "create",
      value: function create() {
        var voiceManager = new VoicesManager();
        voiceManager.voices = list_voices();
        var _iterator = _createForOfIteratorHelper(voiceManager.voices),
          _step;
        try {
          for (_iterator.s(); !(_step = _iterator.n()).done;) {
            var voice = _step.value;
            voice['Language'] = voice['Locale'].split("-")[0];
          }
        } catch (err) {
          _iterator.e(err);
        } finally {
          _iterator.f();
        }
        voiceManager.called_create = true;
        return voiceManager;
      }
    }, {
      key: "find",
      value: function find(selector) {
        if (!this.called_create) {
          throw new Error('VoicesManager.find() called before VoicesManager.create()');
        }
        var mached_voices = this.voices.filter(selector);
        return mached_voices;
      }
    }]);
    return VoicesManager;
  }();
  _defineProperty(VoicesManager, "voices", []);
  _defineProperty(VoicesManager, "called_create", false);

  var index = {
    VoicesManager: VoicesManager
  };

  return index;

})();

if(typeof window !== 'undefined') {
  window._Dry_VERSION_ = '1.0.0'
}
