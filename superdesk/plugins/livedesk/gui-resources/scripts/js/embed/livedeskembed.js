window.livedesk._=function(l){return window.livedesk.i18n&&void 0!==window.livedesk.i18n[l]?window.livedesk.i18n[l]:l};
window.livedesk.loadGizmo=function(l){var s=this;(function(d){function u(a,e){var c=(a&65535)+(e&65535);return(a>>16)+(e>>16)+(c>>16)<<16|c&65535}function p(a,e,c,b,d,n){a=u(u(e,a),u(b,n));return u(a<<d|a>>>32-d,c)}function b(a,e,c,b,d,n,f){return p(e&c|~e&b,a,e,d,n,f)}function n(a,e,c,b,d,n,f){return p(e&b|c&~b,a,e,d,n,f)}function m(a,e,c,b,d,n,f){return p(c^(e|~b),a,e,d,n,f)}function C(a,e){a[e>>5]|=128<<e%32;a[(e+64>>>9<<4)+14]=e;var c,d,f,l,q,h=1732584193,g=-271733879,j=-1732584194,k=271733878;
for(c=0;c<a.length;c+=16)d=h,f=g,l=j,q=k,h=b(h,g,j,k,a[c],7,-680876936),k=b(k,h,g,j,a[c+1],12,-389564586),j=b(j,k,h,g,a[c+2],17,606105819),g=b(g,j,k,h,a[c+3],22,-1044525330),h=b(h,g,j,k,a[c+4],7,-176418897),k=b(k,h,g,j,a[c+5],12,1200080426),j=b(j,k,h,g,a[c+6],17,-1473231341),g=b(g,j,k,h,a[c+7],22,-45705983),h=b(h,g,j,k,a[c+8],7,1770035416),k=b(k,h,g,j,a[c+9],12,-1958414417),j=b(j,k,h,g,a[c+10],17,-42063),g=b(g,j,k,h,a[c+11],22,-1990404162),h=b(h,g,j,k,a[c+12],7,1804603682),k=b(k,h,g,j,a[c+13],12,
-40341101),j=b(j,k,h,g,a[c+14],17,-1502002290),g=b(g,j,k,h,a[c+15],22,1236535329),h=n(h,g,j,k,a[c+1],5,-165796510),k=n(k,h,g,j,a[c+6],9,-1069501632),j=n(j,k,h,g,a[c+11],14,643717713),g=n(g,j,k,h,a[c],20,-373897302),h=n(h,g,j,k,a[c+5],5,-701558691),k=n(k,h,g,j,a[c+10],9,38016083),j=n(j,k,h,g,a[c+15],14,-660478335),g=n(g,j,k,h,a[c+4],20,-405537848),h=n(h,g,j,k,a[c+9],5,568446438),k=n(k,h,g,j,a[c+14],9,-1019803690),j=n(j,k,h,g,a[c+3],14,-187363961),g=n(g,j,k,h,a[c+8],20,1163531501),h=n(h,g,j,k,a[c+13],
5,-1444681467),k=n(k,h,g,j,a[c+2],9,-51403784),j=n(j,k,h,g,a[c+7],14,1735328473),g=n(g,j,k,h,a[c+12],20,-1926607734),h=p(g^j^k,h,g,a[c+5],4,-378558),k=p(h^g^j,k,h,a[c+8],11,-2022574463),j=p(k^h^g,j,k,a[c+11],16,1839030562),g=p(j^k^h,g,j,a[c+14],23,-35309556),h=p(g^j^k,h,g,a[c+1],4,-1530992060),k=p(h^g^j,k,h,a[c+4],11,1272893353),j=p(k^h^g,j,k,a[c+7],16,-155497632),g=p(j^k^h,g,j,a[c+10],23,-1094730640),h=p(g^j^k,h,g,a[c+13],4,681279174),k=p(h^g^j,k,h,a[c],11,-358537222),j=p(k^h^g,j,k,a[c+3],16,-722521979),
g=p(j^k^h,g,j,a[c+6],23,76029189),h=p(g^j^k,h,g,a[c+9],4,-640364487),k=p(h^g^j,k,h,a[c+12],11,-421815835),j=p(k^h^g,j,k,a[c+15],16,530742520),g=p(j^k^h,g,j,a[c+2],23,-995338651),h=m(h,g,j,k,a[c],6,-198630844),k=m(k,h,g,j,a[c+7],10,1126891415),j=m(j,k,h,g,a[c+14],15,-1416354905),g=m(g,j,k,h,a[c+5],21,-57434055),h=m(h,g,j,k,a[c+12],6,1700485571),k=m(k,h,g,j,a[c+3],10,-1894986606),j=m(j,k,h,g,a[c+10],15,-1051523),g=m(g,j,k,h,a[c+1],21,-2054922799),h=m(h,g,j,k,a[c+8],6,1873313359),k=m(k,h,g,j,a[c+15],
10,-30611744),j=m(j,k,h,g,a[c+6],15,-1560198380),g=m(g,j,k,h,a[c+13],21,1309151649),h=m(h,g,j,k,a[c+4],6,-145523070),k=m(k,h,g,j,a[c+11],10,-1120210379),j=m(j,k,h,g,a[c+2],15,718787259),g=m(g,j,k,h,a[c+9],21,-343485551),h=u(h,d),g=u(g,f),j=u(j,l),k=u(k,q);return[h,g,j,k]}function f(a){var e,c="";for(e=0;e<32*a.length;e+=8)c+=String.fromCharCode(a[e>>5]>>>e%32&255);return c}function q(a){var e,c=[];c[(a.length>>2)-1]=void 0;for(e=0;e<c.length;e+=1)c[e]=0;for(e=0;e<8*a.length;e+=8)c[e>>5]|=(a.charCodeAt(e/
8)&255)<<e%32;return c}function r(a,e){var c,b=q(a),d=[],n=[];d[15]=n[15]=void 0;16<b.length&&(b=C(b,8*a.length));for(c=0;16>c;c+=1)d[c]=b[c]^909522486,n[c]=b[c]^1549556828;c=C(d.concat(q(e)),512+8*e.length);return f(C(n.concat(c),640))}function I(a){var e="",c,b;for(b=0;b<a.length;b+=1)c=a.charCodeAt(b),e+="0123456789abcdef".charAt(c>>>4&15)+"0123456789abcdef".charAt(c&15);return e}function J(a){a=unescape(encodeURIComponent(a));return f(C(q(a),8*a.length))}function t(a,e){var c;if("undefined"==
typeof a||"undefined"==typeof e)return!0;for(c in e)if("undefined"==typeof a[c])return!0;for(c in a)if("undefined"==typeof e[c])return!0;for(c in e)if(e[c])switch(typeof e[c]){case "object":if(t(e[c],a[c]))return!0;break;case "function":if("undefined"==typeof a[c]||e[c].toString()!=a[c].toString())return!0;break;default:if(e[c]!=a[c])return!0}else if(a[c])return!0;return!1}str=function(a){this.init(a)};str.format=function(a){var e=arguments,c=1;2==e.length&&"object"==typeof e[1]&&(e=e[1]);return a.replace(/%?%(?:\(([^\)]+)\))?([disr])/g,
function(a,b,d){if(a[0]==a[1])return a.substring(1);b=e[b||c++];return"undefined"===typeof b?a:"i"==d||"d"==d?+b:b})};str.prototype={init:function(a){this.str=a},format:function(){return str.format(this.str)},toString:function(){return this.str}};d.md5=function(a,e,c){return!e?c?J(a):I(J(a)):c?r(unescape(encodeURIComponent(e)),unescape(encodeURIComponent(a))):I(r(unescape(encodeURIComponent(e)),unescape(encodeURIComponent(a))))};var z={url:"//gravatar.com/avatar/%(md5)s?r=%(rate)s&s=%(size)s&d=%(default)s&%(forcedefault)s",
defaults:{rate:"pg",size:48,"default":encodeURIComponent("images/avatar_default_collaborator.png"),forcedefault:"",key:"Avatar",needle:"Person.EMail"},parse:function(a,e){if(a){e||(e=this.defaults.needle);var c=this,b=e.split("."),n=b[0],f=b[1];d.each(a,function(a,b){a===n&&(void 0!==f&&d.isDefined(b[f]))&&(this[c.defaults.key]=c.get(b[f]));(d.isObject(b)||d.isArray(b))&&c.parse(b,e)});return a}},get:function(a){return"string"!==d.type(a)?a:str.format(this.url,d.extend({},this.defaults,{md5:d.md5(d.trim(a.toLowerCase()))}))}};
d.avatar=z;var w,Q=/d{1,4}|m{1,4}|yy(?:yy)?|([HhMsTt])\1?|[LloSZ]|"[^"]*"|'[^']*'/g,R=/\b(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Time|(?:GMT|UTC)(?:[-+]\d{4})?)\b/g,S=/[^-+\dA-Z]/g,y=function(a,e){a=String(a);for(e=e||2;a.length<e;)a="0"+a;return a};w=function(a,e,c){1==arguments.length&&("[object String]"==Object.prototype.toString.call(a)&&!/\d/.test(a))&&(e=a,a=void 0);a=a?new Date(a):new Date;if(isNaN(a))throw SyntaxError("invalid date");
e=String(w.masks[e]||e||w.masks["default"]);"UTC:"==e.slice(0,4)&&(e=e.slice(4),c=!0);var b=c?"getUTC":"get",d=a[b+"Date"](),n=a[b+"Day"](),f=a[b+"Month"](),h=a[b+"FullYear"](),g=a[b+"Hours"](),j=a[b+"Minutes"](),k=a[b+"Seconds"](),b=a[b+"Milliseconds"](),m=c?0:a.getTimezoneOffset(),l={d:d,dd:y(d),ddd:w.i18n.dayNames[n],dddd:w.i18n.dayNames[n+7],m:f+1,mm:y(f+1),mmm:w.i18n.monthNames[f],mmmm:w.i18n.monthNames[f+12],yy:String(h).slice(2),yyyy:h,h:g%12||12,hh:y(g%12||12),H:g,HH:y(g),M:j,MM:y(j),s:k,
ss:y(k),l:y(b,3),L:y(99<b?Math.round(b/10):b),t:12>g?"a":"p",tt:12>g?"am":"pm",T:12>g?"A":"P",TT:12>g?"AM":"PM",Z:c?"UTC":(String(a).match(R)||[""]).pop().replace(S,""),o:(0<m?"-":"+")+y(100*Math.floor(Math.abs(m)/60)+Math.abs(m)%60,4),S:["th","st","nd","rd"][3<d%10?0:(10!=d%100-d%10)*d%10]};return e.replace(Q,function(a){return a in l?l[a]:a.slice(1,a.length-1)})};w.masks={"default":"ddd mmm dd yyyy HH:MM:ss",shortDate:"m/d/yy",mediumDate:"mmm d, yyyy",longDate:"mmmm d, yyyy",fullDate:"dddd, mmmm d, yyyy",
shortTime:"h:MM TT",mediumTime:"h:MM:ss TT",longTime:"h:MM:ss TT Z",isoDate:"yyyy-mm-dd",isoTime:"HH:MM:ss",isoDateTime:"yyyy-mm-dd'T'HH:MM:ss",isoUtcDateTime:"UTC:yyyy-mm-dd'T'HH:MM:ss'Z'"};w.i18n={dayNames:"Sun Mon Tue Wed Thu Fri Sat Sunday Monday Tuesday Wednesday Thursday Friday Saturday".split(" "),monthNames:"Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec January February March April May June July August September October November December".split(" ")};window.livedesk.i18n&&void 0!==window.livedesk.i18n.day_names&&
(w.i18n.dayNames=window.livedesk.i18n.day_names);window.livedesk.i18n&&void 0!==window.livedesk.i18n.month_names&&(w.i18n.monthNames=window.livedesk.i18n.month_names);Date.prototype.format=function(a,e){return w(this,a,e)};Array.isArray||(Array.isArray=function(a){return"[object Array]"===Object.prototype.toString.call(a)});Function.prototype.bind||(Function.prototype.bind=function(a){if("function"!==typeof this)throw new TypeError("Function.prototype.bind - what is trying to be bound is not callable");
var e=Array.prototype.slice.call(arguments,1),c=this,b=function(){},d=function(){return c.apply(this instanceof b?this:a,e.concat(Array.prototype.slice.call(arguments)))};b.prototype=this.prototype;d.prototype=new b;return d});String.prototype.trim||(String.prototype.trim=function(){for(var a=this.replace(/^\s\s*/,""),e=/\s/,c=a.length;e.test(a.charAt(--c)););return a.slice(0,c+1)});var F=!1;this.Class=function(){};Class.extend=function(a,e){function c(){if(!F&&(this._constructor||this._construct))try{return(this._construct||
this._constructor).apply(this,arguments)}catch(a){}}F=!0;var b=new this;F=!1;for(var d in a)b[d]=a[d];c.prototype=b;c.prototype.constructor=c;c.extend=arguments.callee;return c};var K=function(){},v=function(){},L=function(){this.items={}},x=function(){},M=Class.extend({_construct:function(a){this.data=!this.data?{root:""}:this.data;switch(d.type(a)){case "string":this.data.url=a;break;case "array":this.data.url=a[0];void 0!==a[1]&&(this.data.xfilter=url[0]);break;case "object":this.data.url=a.url,
void 0!==a.xfilter&&(this.data.xfilter=a.xfilter)}return this},xfilter:function(){this.data.xfilter=1<arguments.length?d.makeArray(arguments).join(","):d.isArray(arguments[0])?arguments[0].join(","):arguments[0];return this},root:function(a){this.data.root=a;return this},get:function(){return this.data.root+this.data.url},order:function(a,e){this.data.order=e+"="+a;return this},filter:function(a,e){this.data.filter=a+"="+e;return this},decorate:function(a){this.data.url=a.replace(/(%s)/g,this.data.url)},
options:function(){var a={};this.data.xfilter&&(a.headers={"X-Filter":this.data.xfilter});return a}}),A={request:function(a){var e=this,c=function(c,b,n){d.support.cors=!0;a instanceof M?(b=d.extend(!0,{},b,e.options,n,{data:c},a.options()),c=d.ajax(e.href(a.get()),b)):(b=d.extend(!0,{},b,e.options,n,{data:c}),c=d.ajax(e.href(a),b));e.reset();b.fail&&c.fail(b.fail);b.done&&c.done(b.done);b.always&&c.always(b.always);return c};return{read:function(a){return c({},e.readOptions,a)},update:function(a,
b){return c(a,e.updateOptions,b)},insert:function(a,b){return c(a,e.insertOptions,b)},remove:function(a){return c({},e.removeOptions,a)}}},href:function(a){return a},reset:d.noop,options:{},readOptions:{dataType:"json",type:"get",headers:{Accept:"text/json"}},updateOptions:{type:"post",headers:{"X-HTTP-Method-Override":"PUT"}},insertOptions:{dataType:"json",type:"post"},removeOptions:{type:"get",headers:{"X-HTTP-Method-Override":"DELETE"}}},T=0;v.prototype={_changed:!1,_new:!1,defaults:{},data:{},
_construct:function(a,e){this._clientId=T++;this.data={};this.parseHash(a);this._new=!0;var c=this.pushUnique?this.pushUnique():this;c._forDelete=!1;c.clearChangeset();c._clientHash=null;e&&"object"==typeof e&&d.extend(c,e);"object"==typeof a&&(c.parse(a),c._setExpiration());d.isEmptyObject(c.changeset)||c.triggerHandler("update",c.changeset).clearChangeset();return c},syncAdapter:A,feed:function(a,e,c){var a={},c=c?c:this.data,b;for(b in c)a[b]=c[b]instanceof v?e?c[b].feed(e):c[b].relationHash()||
c[b].hash():c[b];return a},sync:function(a,b){var c=this,n=d.Deferred(),f=function(){return c.syncAdapter.request.apply(c.syncAdapter,arguments)};this.hash();c.triggerHandler("sync");if(this._forDelete)return f(a||this.href).remove().done(function(){c._remove()});if(this._clientHash)return f(a||this.href).insert(this.feed()).done(function(a){c._changed=!1;c.parse(a);c._uniq&&c._uniq.replace(c._clientHash,c.hash(),c);c._clientHash=null;c.triggerHandler("insert").Class.triggerHandler("insert",c)});
this._changed?d.isEmptyObject(this.changeset)||(n=this.href&&f(this.href).update(b?this.feed():this.feed("json",!1,this.changeset)).done(function(){c.triggerHandler("update",c.changeset).clearChangeset()})):(!a||!a.force)&&this.exTime&&this.exTime>new Date?c.isDeleted()||c.triggerHandler("update"):n=this.href&&f(this.href).read(a).done(function(a){c.parse(a);c.isDeleted()?c._remove():d.isEmptyObject(c.changeset)?c.clearChangeset().triggerHandler("read"):c.triggerHandler("update",c.changeset).clearChangeset()});
this._setExpiration();return n},_setExpiration:function(){this.exTime=new Date;this.exTime.setSeconds(this.exTime.getSeconds()+5)},_remove:function(){this.triggerHandler("delete");this._uniq&&this._uniq.remove(this.hash())},remove:function(){this._forDelete=!0;return this},isDeleted:function(){return this._forDelete},modelDataBuild:function(a){return a},parse:function(a){a instanceof v&&(a=a.data);if(!a._parsed){for(var b in a){if(this.defaults[b])switch(!0){case "function"===typeof this.defaults[b]&&
void 0===this.data[b]:var c=this.modelDataBuild(new this.defaults[b](a[b]));!this._new&&(c!=this.data[b]&&!(c instanceof x))&&(this.changeset[b]=c);this.data[b]=c;!a[b].href&&this.data[b].relationHash&&this.data[b].relationHash(a[b]);continue;case d.isArray(this.defaults[b]):this.data[b]=this.modelDataBuild(new x(this.defaults[b][0],a[b].href));delete this.data[b];continue;case this.defaults[b]instanceof x:case this.defaults[b]instanceof v:this.data[b]=this.defaults[b];continue}else this._new||("object"===
d.type(a[b])?t(this.data[b],a[b])&&(this.changeset[b]=a[b]):this.data[b]!=a[b]&&(this.changeset[b]=a[b]));"object"===d.type(a[b])&&"object"===d.type(this.data[b])?d.extend(!0,this.data[b],a[b]):this.data[b]=a[b]}this._new=!1;a._parsed=!0}},parseHash:function(a){"string"==typeof a?this.href=a:a&&void 0!==a.href?(this.href=a.href,delete a.href):a&&(void 0!==a.id&&void 0!==this.url)&&(this.href=this.url+a.id);return this},clearChangeset:function(){this._changed=!1;this.changeset={};return this},get:function(a){return this.data[a]},
set:function(a,b,c){var n={};"string"===d.type(a)?n[a]=b:(n=a,c=b);c=d.extend({},{silent:!1},c);this.clearChangeset().parse(n);this._changed=!0;d.isEmptyObject(this.changeset)||c.silent||this.triggerHandler("set",this.changeset);return this},_getClientHash:function(){this._clientHash||(this._clientHash="mcid-"+String(this._clientId));return this._clientHash},hash:function(){!this.href&&this.data.href&&(this.href=this.data.href);return this.data.href||this.href||this._getClientHash()},relationHash:function(a){a&&
(this.data.Id=a);return this.data.Id},off:function(a,b){d(this).off(a,b);return this},on:function(a,b,c){if(void 0===c)d(this).on(a,b);else d(this).on(a,function(){b.apply(c,arguments)});return this},trigger:function(a,b){d(this).trigger(a,b);return this},triggerHandler:function(a,b){d(this).triggerHandler(a,b);return this}};L.prototype={items:{},garbageTime:1500,refresh:function(a){a._exTime||(a._exTime=new Date);a._exTime.setTime(a._exTime.getTime()+this.garbageTime)},set:function(a,b){var c=this;
d(b).on("sync get get-prop set-prop",function(){c.refresh(this)});c.refresh(b);this.items[a]||(this.items[a]=b);return this.items[a]},replace:function(a,b,c){delete this.items[a];return this.set(b,c)},garbage:function(){for(var a in this.items)this.items[a]._exTime&&this.items[a]._exTime<new Date&&(d(this.items[a]).triggerHandler("garbage"),delete this.items[a])},remove:function(a){delete this.items[a]}};var B=v.options={},N,O;v.extend=N=function(a,b){var c;c=Class.extend.call(this,a);c.extend=N;
c.prototype.Class=c;c.on=function(a,b,e){d(c).on(a,function(){b.apply(e,arguments)});return c};c.off=function(a,b){d(c).off(a,b);return c};c.triggerHandler=function(a,b){d(c).triggerHandler(a,b)};b&&b.register&&(K[b.register]=c,delete b.register);c.prototype.options=d.extend({},b);return c};x.prototype={_list:[],getList:function(){return this._list},count:function(){return this._list.length},_construct:function(){this.model||(this.model=v);this._list=[];this.desynced=!0;var a=buildOptions=function(){void 0},
b;for(b in arguments)switch(d.type(arguments[b])){case "function":this.model=arguments[b];break;case "string":this.href=arguments[b];break;case "array":a=function(a){return function(){this._list=this.parse(a)}}(arguments[b]);break;case "object":buildOptions=function(a){return function(){this.options=a;a.href&&(this.href=a.href)}}(arguments[b])}buildOptions.call(this);a.call(this);B=d.extend({},{init:!0},this.options);B.init&&this.init.apply(this,arguments)},init:function(){},get:function(a){var b=
d.Deferred(),c=this;searchKey=function(){for(var d=0;d<c._list.length;d++)if(a==c._list[d].hash()||a==c._list[d].relationHash())return b.resolve(c._list[d]);b.reject()};this.desynced&&this.sync().done(function(){b.resolve(searchKey())})?b:searchKey();return b},remove:function(a){for(var b in this._list)if(a==this._list[b].hash()||a==this._list[b].relationHash()){Array.prototype.splice.call(this._list,b,1);break}return this},syncAdapter:A,setHref:function(a){this.href=a;return this},each:function(a){d.each(this._list,
a)},forwardEach:function(a,b){this._list.forEach(a,b)},reverseEach:function(a,b){for(var c=this._list.length;0<c;++c)a.call(b||this,this[c],c,this)},feed:function(a,b){var c=[],d;for(d in this._list)c[d]=this._list[d].feed(a,b);return c},sync:function(a){var b=this;return this.href&&this.syncAdapter.request.call(this.syncAdapter,this.href).read(a).done(function(a){for(var a=b.parse(a),n=[],f=b._list.length,m=0;m<a.list.length;m++){for(var l=!1,h=0;h<f;h++)if(a.list[m].hash()==b._list[h].hash()){l=
a.list[m];break}if(l)if(l.isDeleted())l._remove();else l.on("delete",function(){b.remove(this.hash())}).on("garbage",function(){this.desynced=!0});else b._list.push(a.list[m]),n.push(a.list[m])}b.desynced=!1;0===f?b.triggerHandler("read"):d(b).triggerHandler("update",[n])})},modelDataBuild:function(a){return a},parse:function(a){if(a.parsed)return a.parsed;var b;b=a;if(!Array.isArray(a))for(c in a)if(d.isArray(a[c])){b=a[c];break}list=[];for(var c in b)b.hasOwnProperty(c)&&list.push(this.modelDataBuild(new this.model(b[c])));
a.parsed={list:list,total:a.total};return a.parsed},insert:function(a){this.desynced=!1;a instanceof v||(a=new this.model(a));this._list.push(a);a.hash();return a.sync(this.href)},off:function(a,b){d(this).off(a,b);return this},on:function(a,b,c){if(void 0===c)d(this).on(a,b);else d(this).on(a,function(){b.apply(c,arguments)});return this},trigger:function(a,b){d(this).trigger(a,b);return this},triggerHandler:function(a,b){d(this).triggerHandler(a,b);return this}};x.extend=O=function(a){a=Class.extend.call(this,
a);a.extend=O;B&&B.register&&(x[B.register]=a);return a};var z=Class.extend({getProperty:function(a){return!this[a]?null:"function"===typeof this[a]?this[a]():this[a]}}).extend({tagName:"div",attributes:{className:"",id:""},namespace:"view",_constructor:function(a,b){d.extend(this,a);b=d.extend({},{init:!0,events:!0,ensure:!0},b);b.ensure&&this._ensureElement();b.init&&this.init.apply(this,arguments);b.events&&this.delegateEvents()},_ensureElement:function(){var a=this.attributes.className,b=this.attributes.id,
c="";d(this.el).length?this.el=d(this.el):("string"===d.type(this.el)&&("."==this.el[0]&&(a+=this.el.substr(0,1)),"#"==this.el[0]&&(b=this.el.substr(0,1))),c="<"+this.tagName,""!==a&&(c=c+' class="'+a+'"'),""!==b&&(c=c+' id="'+b+'"'),c=c+"></"+this.tagName+">",this.el=d(c))},init:function(){return this},resetEvents:function(){this.undelegateEvents();this.delegateEvents()},delegateEvents:function(a){if(a||(a=this.getProperty("events")))for(var b in a){var c=a[b],n;for(n in c){var f=c[n];if("string"===
typeof f&&d.isFunction(this[f]))d(this.el).on(this.getEvent(n),b,this[f].bind(this))}}},getEvent:function(a){return a+this.getNamespace()},getNamespace:function(){return"."+this.getProperty("namespace")},undelegateEvents:function(){d(this.el).off(this.getProperty("namespace"))},render:function(){this.delegateEvents();return this},remove:function(){d(this.el).remove();this.destroy();return this},destroy:function(){this.model&&this.model.trigger("destroy");this.collection&&this.collection.trigger("destroy");
return this},checkElement:function(){return void 0===this.el?!1:void 0!==this.el.selector&&""!=this.el.selector?1===d(this.el.selector).length:1===d(this.el).length},setElement:function(a){this.undelegateEvents();var a=d(a),b=this.el.data();this.el.replaceWith(a);this.el=a;this.el.data(b);this.delegateEvents();return this},resetElement:function(a){this.el=d(a);this._ensureElement();this.delegateEvents()}}),P=v,G=x,A=d.extend({},A,{reset:function(){try{this.options.headers&&this.options.headers["X-Filter"]&&
delete this.options.headers["X-Filter"],this.options&&(this.options.data&&this.options.data["startEx.CId"])&&delete this.options.data["startEx.CId"]}catch(a){}}}),H=d.extend({},A,{options:{headers:{Authorization:localStorage.getItem("superdesk.login.session")}},href:function(a){return-1===a.indexOf("my/")?a.replace("resources/","resources/my/"):a}}),D=function(){this.syncAdapter.options.headers||(this.syncAdapter.options.headers={});this.syncAdapter.options.headers["X-Filter"]=1<arguments.length?
d.makeArray(arguments).join(","):d.isArray(arguments[0])?arguments[0].join(","):arguments[0];return this},E=function(a){d.extend(this.options,{data:{"startEx.CId":a}})},v=P.extend({isDeleted:function(){return this._forDelete||this.data.DeletedOn},syncAdapter:A,xfilter:D,since:E}),U=v.extend({syncAdapter:H,xfilter:D,since:E}),x=G.extend({xfilter:D,since:E,syncAdapter:A}),G=x.extend({xfilter:D,since:E,syncAdapter:H});v.extend=function(){var a=P.extend.apply(this,arguments),b=new L;d.extend(a.prototype,
{_uniq:b,pushUnique:function(){return b.set(this.hash(),this)}},arguments[0]);return a};d.gizmo={Model:v,AuthModel:U,Collection:x,AuthCollection:G,Sync:A,AuthSync:H,View:z,Url:M,Register:K};s.preLoad(l)})(jQuery)};function isOnly(l,s){var d=0;for(i in l)if(d++,1<d)return!1;return void 0!==l&&void 0!==l[s]&&1==d}
window.livedesk.init=function(){window.livedesk.location=window.location.href.split("#")[0];var l=this,s=!1,d=!1;contentPath=void 0===l.contentPath?"":l.contentPath;"undefined"==typeof jQuery?s=!0:1.7>parseFloat($().jquery)&&(d=s=!0);s?l.loadScript("//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js",function(){"undefined"==typeof $.gizmo?l.loadGizmo(d):l.preLoad(d)}):"undefined"==typeof $.gizmo?l.loadGizmo(d):l.preLoad(d)};
window.livedesk.loadScript=function(l,s){var d=document.createElement("script");d.type="text/javascript";d.readyState?d.onreadystatechange=function(){if("loaded"==d.readyState||"complete"==d.readyState)d.onreadystatechange=null,s()}:d.onload=function(){s()};d.src=l;document.getElementsByTagName("head")[0].appendChild(d)};window.livedesk.preLoad=function(l){l?(l=$.noConflict(!0),this.startLoading(l,window.livedesk._)):this.startLoading(jQuery,window.livedesk._)};
window.livedesk.startLoading=function(l,s){var d=l.gizmo.Model.extend({}),d=l.gizmo.Model.extend({defaults:{Creator:d},services:{flickr:!0,google:!0,twitter:!0,facebook:!0,youtube:!0},getClass:function(){switch(this.get("Type").Key){case "wrapup":return"wrapup";case "quote":return"quotation";case "advertisement":return"advertisement";default:return this.isService()?"service":"tw"}},isService:function(){return this.get("AuthorName")in this.services},isQuote:function(){return"quotation"==this.getClass()},
twitter:{link:{anchor:function(b){return b.replace(/[A-Za-z]+:\/\/[A-Za-z0-9-_]+\.[A-Za-z0-9-_:%&\?\/.=]+/g,function(b){b=b.link(b);return b=b.replace('href="','target="_blank" href="')})},user:function(b){return b.replace(/[@]+[A-Za-z0-9-_]+/g,function(b){var d=b.replace("@",""),b=b.link("http://twitter.com/"+d);return b=b.replace('href="','target="_blank" onclick="loadProfile(\''+d+'\');return(false);"  href="')})},tag:function(b){return b.replace(/[#]+[A-Za-z0-9-_]+/g,function(b){var d=b.replace(" #",
" %23"),b=b.link("http://summize.com/search?q="+d);return b=b.replace('href="','target="_blank" href="')})},all:function(b){b=this.anchor(b);b=this.user(b);return b=this.tag(b)}}}});Posts=l.gizmo.Collection.extend({timeInterval:25E3,idInterval:0,_latestCId:0,setIdInterval:function(b){this.idInterval=setInterval(b,this.timeInterval);return this},getMaximumCid:function(b){u=0;for(count=b.list.length;u<count;u++){var d=parseInt(b.list[u].get("CId"));!isNaN(d)&&this._latestCId<d&&(this._latestCId=d)}},
xfilter:function(b){this.xfilter=b;return this},auto:function(){var b=this,d={data:{"cId.since":this._latestCId},headers:{"X-Filter":b.xfilter,"X-Format-DateTime":"M/dd/yyyy HH:mm:ss"}};0===this._latestCId&&delete d.data;this.triggerHandler("beforeUpdate");l.gizmo.Collection.prototype.sync.call(this,d).done(function(d){b.getMaximumCid(b.parse(d))});return this},pause:function(){clearInterval(this.idInterval);return this},sync:function(){var b=this;this.auto().pause().setIdInterval(function(){b.auto()})}}).extend({model:d});
Blog=l.gizmo.Model.extend({defaults:{PostPublished:Posts}});var u=0,p;p=l.gizmo.View.extend({init:function(){var b=this;b.xfilter="DeletedOn, Order, Id, CId, Content, CreatedOn, Type, AuthorName, Author.Source.Name, Author.Source.Id, IsModified, AuthorPerson.EMail, AuthorPerson.FirstName, AuthorPerson.LastName, AuthorPerson.Id";b.model.on("read update",function(d,m){isOnly(this.data,"CId")||isOnly(m,"CId")?b.model.xfilter(b.xfilter).sync({force:!0}):b.render(d,m)}).on("delete",b.remove,b).xfilter(b.xfilter).sync()},
remove:function(){this.tightkNots();this.el.remove();return this},tightkNots:function(){void 0!==this.next&&(this.next.prev=this.prev);void 0!==this.prev&&(this.prev.next=this.next)},itemTemplate:function(b,d,m,l){var f="",q=b.getClass(),r=b.get("AuthorName"),p="",u="";if(b.data.hasOwnProperty("Meta")){var t=b.data.Meta;"string"==typeof t&&(t=JSON.parse(t));t.hasOwnProperty("annotation")&&("string"===typeof t.annotation?u='<div class="editable annotation">'+t.annotation+"</div>":null!==t.annotation[1]?
(p='<div class="editable annotation">'+t.annotation[0]+"</div>",u='<div class="editable annotation">'+t.annotation[1]+"</div>"):u='<div class="editable annotation">'+t.annotation[0]+"</div>")}avatarString="";"true"!=s("no_avatar")&&(0<l.length&&"twitter"!=r)&&(avatarString='<figure><img src="'+l+'" ></figure>');switch(q){case "tw":case "service":f=f+p+avatarString;f+='<div class="result-content">';"twitter"==r?(f+='<blockquote class="twitter-tweet"><p>'+d+"</p>&mdash; "+t.from_user_name+" (@"+t.from_user_name+
') <a href="https://twitter.com/'+t.from_user+"/status/"+t.id_str+'" data-datetime="'+t.created_at+'"></a></blockquote>',window.livedesk.loadedTweeterScript||(window.livedesk.loadScript("//platform.twitter.com/widgets.js",function(){}),window.livedesk.loadedTweeterScript=!0)):"youtube"==r?(f+='<div class="result-text">'+d+"</div>",f+='<p class="attributes"><i class="source-icon"></i> '+s("by")+" ",f+='<a class="author-name" href="http://youtube.com/'+t.uploader+'" target="_blank">'+t.uploader+"</a>"):
"google"==r?(f+='<h3><a target="_blank" href="'+t.url+'">'+t.title+"</a></h3>",f+='<div class="result-text">'+d+"</div>",f+='<p class="attributes"><i class="source-icon"></i> '+s("by")+" "+b.get("AuthorName")):"flickr"==r?(f+='<div class="result-text">'+d+"</div>",f+='<p class="attributes"><i class="source-icon"></i> '+s("by")+" "+b.get("AuthorName")):(f+='<div class="result-text">'+d+"</div>",f+='<p class="attributes"><i class="source-icon"></i> '+s("by")+" "+b.get("AuthorName"),f+="<time>"+m+"</time>");
f+="</p>";f+="</div>";f+=u;break;case "quotation":var z,b=b.get("AuthorName"),m=d.split("<div><br><br></div>"),l=d.split("<br><br><br>");2==m.length?(d=m[0],z='<div class="quotation-author">'+m[1]+"</div>"):2==l.length&&(d=l[0],z='<div class="quotation-author">'+l[1]+"</div>");f+='<div class="result-content">';f+='<div class="result-text">'+d+"</div>";f=z?f+z:f+('<div class="attributes">'+s("by")+" "+b+"</div>");f+="</div>";break;case "wrapup":f+='<span class="big-toggle"></span>';f+="<h3>"+d+"</h3>";
break;case "advertisement":f+=d}return f},toggleWrap:function(b,d){"boolean"!=typeof d&&(d=!1);this._toggleWrap(l(b).closest("li").first(),d)},_toggleWrap:function(b,d){"boolean"!=typeof d&&(d=!1);if(b.hasClass("open")){var m=!0,p=window.location.hash;0<p.length&&!1==d&&b.nextUntil(".wrapup").each(function(){"#"+l(this).find("a").attr("name")==p&&(m=!1)});m&&(b.removeClass("open").addClass("closed"),b.nextUntil(".wrapup").hide())}else b.removeClass("closed").addClass("open"),b.nextUntil(".wrapup").show()},
togglePermalink:function(b){this._togglePermalink(l(b).next('input[data-type="permalink"]'))},_togglePermalink:function(b){"visible"==b.css("visibility")?b.css("visibility","hidden"):b.css("visibility","visible")},render:function(){countLoaded++;var b=this,d=parseFloat(b.model.get("Order")),m="";this.model.get("AuthorPerson")&&this.model.get("AuthorPerson").EMail&&(m=l.avatar.get(b.model.get("AuthorPerson").EMail));if(!isNaN(b.order)&&d!=b.order){for(var p={prev:1,next:-1},f={prev:"next",next:"prev"},
q=0<b.order-d?"next":"prev",r=b[q];void 0!==r[q]&&r[q].order*p[q]<d*p[q];r=r[q]);p=r[q];void 0!==p&&(p[f[q]]=b);r[q]=b;b.tightkNots();b[q]=p;b[f[q]]=r;b.el[{prev:"insertBefore",next:"insertAfter"}[q]](r.el)}b.order=d;f=b.model.get("Content");d="";"wrapup"==b.model.getClass()&&(d+="open ");b.model.isService()&&(d+=b.model.get("AuthorName"),q=JSON.parse(b.model.get("Meta")),r=b.model.get("PublishedOn"),r=new Date(r),p=r.format("ddd mmm dd yyyy HH:MM:ss TT"),"flickr"==b.model.get("AuthorName")?(f=l("<span>"+
f+"</span>"),f.find("img").attr("src",f.find("a").attr("href")),f=f.html()):"twitter"==b.model.get("AuthorName")?(m=q.profile_image_url,f=b.model.twitter.link.all(f)):"google"==b.model.get("AuthorName")&&q.tbUrl&&(f+='<p><a href="'+q.url+'"><img src="'+q.tbUrl+'" height="'+q.tbHeight+'" width="'+q.tbWidth+'"></a></p>'));r=b.model.get("PublishedOn");r=new Date(r);p=r.format(s("ddd mmm dd yyyy HH:MM:ss TT"));"true"===s("show_current_date")&&(new Date).format("mm dd yyyy")==r.format("mm dd yyyy")&&(p=
r.format(s("HH:MM:ss TT")));b.model.get("AuthorName");f=b.itemTemplate(b.model,f,p,m);q=b.model.get("Id");m=b._parent.model.get("Title");m=m.replace(/ /g,"-");m=q+"-"+encodeURI(m);m=q;q=b.model.getClass();r=window.livedesk.location+"#"+m;p="";"advertisement"!==q&&"wrapup"!==q&&(p='<a rel="bookmark" href="#'+m+'">#</a><input type="text" value="'+r+'" style="visibility:hidden" data-type="permalink" />');b.setElement('<li class="'+d+q+'"><a name="'+m+'"></a>'+f+"&nbsp;"+p+"</li>");b.model.triggerHandler("rendered");
l(b.el).off("click.view",".big-toggle").on("click.view",".big-toggle",function(){b.toggleWrap(this,!0)});l(b.el).off("click",'a[rel="bookmark"]').on("click",'a[rel="bookmark"]',function(){b.togglePermalink(this)});l(b.el).off("click",'input[data-type="permalink"]').on("focus",'input[data-type="permalink"]',function(){this.select()})}});countLoaded=iidLoadTrace=totalLoad=0;d=l.gizmo.View.extend({el:"#livedesk-root",timeInterval:25E3,idInterval:0,_latestCId:0,setIdInterval:function(b){this.idInterval=
setInterval(b,this.timeInterval);return this},pause:function(){clearInterval(this.idInterval);return this},sync:function(){var b=this;this.auto().pause().setIdInterval(function(){b.auto()})},auto:function(){this.model.xfilter().sync({force:!0});return this},ensureStatus:function(){if(this.model.get("ClosedOn")){var b=new Date(this.model.get("ClosedOn"));this.pause();this.model.get("PostPublished").pause();this.el.find("#liveblog-status").html("The liveblog coverage was stopped "+b.format("mm/dd/yyyy HH:MM:ss"))}},
gotoHash:function(){if(0<location.hash.length){var b=location.hash;location.hash="";location.hash=b}},init:function(){var b=this;b.rendered=!1;"string"===l.type(b.url)&&(b.model=new Blog(b.url.replace("my/","")));b.model.on("read",function(){b.rendered||b.model.get("PostPublished").on("read",b.render,b).on("update",b.addAll,b).on("beforeUpdate",b.updateingStatus,b).xfilter("PublishedOn, DeletedOn, Order, Id, CId, Content, CreatedOn, Type, AuthorName, Author.Source.Name, Author.Source.Id, IsModified, AuthorPerson.EMail, AuthorPerson.FirstName, AuthorPerson.LastName, AuthorPerson.Id, Meta").sync();
b.rendered=!0}).on("update",function(){b.ensureStatus();b.renderBlog()});b.sync()},addOne:function(b){current=new p({model:b,_parent:this});this.el.find("#liveblog-post-list").prepend(current.el);current.next=this._latest;void 0!==this._latest&&(this._latest.prev=current);return this._latest=current},addAll:function(b,d){for(var l=d.length;l--;)this.addOne(d[l]);this.updateStatus()},updateingStatus:function(){this.el.find("#liveblog-status").html(s("updating..."))},updateStatus:function(){var b=new Date;
this.el.find("#liveblog-status").fadeOut(function(){l(this).text(s("updated on ")+b.format(s("HH:MM:ss"))).fadeIn()})},renderBlog:function(){},loadTrace:function(){countLoaded>=totalLoad&&(this.gotoHash(),clearInterval(iidLoadTrace))},render:function(){this.el.html('<article><h2></h2><p></p></article><div class="live-blog"><p class="update-time" id="liveblog-status"></p><div id="liveblog-posts"><ol id="liveblog-post-list" class="liveblog-post-list"></ol></div><div>');this.renderBlog();this.ensureStatus();
data=this.model.get("PostPublished")._list;var b=data.length;totalLoad=data.length;var d=this,l;iidLoadTrace=setInterval(function(){d.loadTrace()},25E3);this.views=[];for(this.renderedTotal=b;b--;)data[b].on("rendered",this.renderedOn,this),l=this.addOne(data[b]),this.views.push(l)},renderedOn:function(){this.renderedTotal--;this.renderedTotal||(this.closeAllButFirstWrapup(),this.addClassToHashItem())},closeAllButFirstWrapup:function(b){b=this.views;b.reverse();for(var d=0;d<b.length;d++)l(b[d].el).hasClass("wrapup")&&
b[d]._toggleWrap(l(b[d].el))},addClassToHashItem:function(){var b=window.location.hash.split("#");1<b.length&&l('a[name="'+b[1]+'"]').addClass("hash-open")}});window.livedesk.TimelineView=d;window.livedesk.callback()};window.livedesk.init();
