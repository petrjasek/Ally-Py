window.livedesk._=function(m){return window.livedesk.i18n&&void 0!==window.livedesk.i18n[m]?window.livedesk.i18n[m]:m};
window.livedesk.loadGizmo=function(m){var r=this;(function(c){function p(a,e){var d=(a&65535)+(e&65535);return(a>>16)+(e>>16)+(d>>16)<<16|d&65535}function q(a,e,d,b,c,n){a=p(p(e,a),p(b,n));return p(a<<c|a>>>32-c,d)}function b(a,e,d,b,c,n,h){return q(e&d|~e&b,a,e,c,n,h)}function n(a,e,d,b,c,n,h){return q(e&b|d&~b,a,e,c,n,h)}function h(a,e,d,b,c,n,h){return q(d^(e|~b),a,e,c,n,h)}function A(a,e){a[e>>5]|=128<<e%32;a[(e+64>>>9<<4)+14]=e;var d,c,l,m,A,g=1732584193,f=-271733879,j=-1732584194,k=271733878;
for(d=0;d<a.length;d+=16)c=g,l=f,m=j,A=k,g=b(g,f,j,k,a[d],7,-680876936),k=b(k,g,f,j,a[d+1],12,-389564586),j=b(j,k,g,f,a[d+2],17,606105819),f=b(f,j,k,g,a[d+3],22,-1044525330),g=b(g,f,j,k,a[d+4],7,-176418897),k=b(k,g,f,j,a[d+5],12,1200080426),j=b(j,k,g,f,a[d+6],17,-1473231341),f=b(f,j,k,g,a[d+7],22,-45705983),g=b(g,f,j,k,a[d+8],7,1770035416),k=b(k,g,f,j,a[d+9],12,-1958414417),j=b(j,k,g,f,a[d+10],17,-42063),f=b(f,j,k,g,a[d+11],22,-1990404162),g=b(g,f,j,k,a[d+12],7,1804603682),k=b(k,g,f,j,a[d+13],12,
-40341101),j=b(j,k,g,f,a[d+14],17,-1502002290),f=b(f,j,k,g,a[d+15],22,1236535329),g=n(g,f,j,k,a[d+1],5,-165796510),k=n(k,g,f,j,a[d+6],9,-1069501632),j=n(j,k,g,f,a[d+11],14,643717713),f=n(f,j,k,g,a[d],20,-373897302),g=n(g,f,j,k,a[d+5],5,-701558691),k=n(k,g,f,j,a[d+10],9,38016083),j=n(j,k,g,f,a[d+15],14,-660478335),f=n(f,j,k,g,a[d+4],20,-405537848),g=n(g,f,j,k,a[d+9],5,568446438),k=n(k,g,f,j,a[d+14],9,-1019803690),j=n(j,k,g,f,a[d+3],14,-187363961),f=n(f,j,k,g,a[d+8],20,1163531501),g=n(g,f,j,k,a[d+13],
5,-1444681467),k=n(k,g,f,j,a[d+2],9,-51403784),j=n(j,k,g,f,a[d+7],14,1735328473),f=n(f,j,k,g,a[d+12],20,-1926607734),g=q(f^j^k,g,f,a[d+5],4,-378558),k=q(g^f^j,k,g,a[d+8],11,-2022574463),j=q(k^g^f,j,k,a[d+11],16,1839030562),f=q(j^k^g,f,j,a[d+14],23,-35309556),g=q(f^j^k,g,f,a[d+1],4,-1530992060),k=q(g^f^j,k,g,a[d+4],11,1272893353),j=q(k^g^f,j,k,a[d+7],16,-155497632),f=q(j^k^g,f,j,a[d+10],23,-1094730640),g=q(f^j^k,g,f,a[d+13],4,681279174),k=q(g^f^j,k,g,a[d],11,-358537222),j=q(k^g^f,j,k,a[d+3],16,-722521979),
f=q(j^k^g,f,j,a[d+6],23,76029189),g=q(f^j^k,g,f,a[d+9],4,-640364487),k=q(g^f^j,k,g,a[d+12],11,-421815835),j=q(k^g^f,j,k,a[d+15],16,530742520),f=q(j^k^g,f,j,a[d+2],23,-995338651),g=h(g,f,j,k,a[d],6,-198630844),k=h(k,g,f,j,a[d+7],10,1126891415),j=h(j,k,g,f,a[d+14],15,-1416354905),f=h(f,j,k,g,a[d+5],21,-57434055),g=h(g,f,j,k,a[d+12],6,1700485571),k=h(k,g,f,j,a[d+3],10,-1894986606),j=h(j,k,g,f,a[d+10],15,-1051523),f=h(f,j,k,g,a[d+1],21,-2054922799),g=h(g,f,j,k,a[d+8],6,1873313359),k=h(k,g,f,j,a[d+15],
10,-30611744),j=h(j,k,g,f,a[d+6],15,-1560198380),f=h(f,j,k,g,a[d+13],21,1309151649),g=h(g,f,j,k,a[d+4],6,-145523070),k=h(k,g,f,j,a[d+11],10,-1120210379),j=h(j,k,g,f,a[d+2],15,718787259),f=h(f,j,k,g,a[d+9],21,-343485551),g=p(g,c),f=p(f,l),j=p(j,m),k=p(k,A);return[g,f,j,k]}function l(a){var e,d="";for(e=0;e<32*a.length;e+=8)d+=String.fromCharCode(a[e>>5]>>>e%32&255);return d}function H(a){var e,d=[];d[(a.length>>2)-1]=void 0;for(e=0;e<d.length;e+=1)d[e]=0;for(e=0;e<8*a.length;e+=8)d[e>>5]|=(a.charCodeAt(e/
8)&255)<<e%32;return d}function t(a,e){var d,b=H(a),c=[],n=[];c[15]=n[15]=void 0;16<b.length&&(b=A(b,8*a.length));for(d=0;16>d;d+=1)c[d]=b[d]^909522486,n[d]=b[d]^1549556828;d=A(c.concat(H(e)),512+8*e.length);return l(A(n.concat(d),640))}function C(a){var e="",d,b;for(b=0;b<a.length;b+=1)d=a.charCodeAt(b),e+="0123456789abcdef".charAt(d>>>4&15)+"0123456789abcdef".charAt(d&15);return e}function B(a){a=unescape(encodeURIComponent(a));return l(A(H(a),8*a.length))}function s(a,e){var d;if("undefined"==
typeof a||"undefined"==typeof e)return!0;for(d in e)if("undefined"==typeof a[d])return!0;for(d in a)if("undefined"==typeof e[d])return!0;for(d in e)if(e[d])switch(typeof e[d]){case "object":if(s(e[d],a[d]))return!0;break;case "function":if("undefined"==typeof a[d]||e[d].toString()!=a[d].toString())return!0;break;default:if(e[d]!=a[d])return!0}else if(a[d])return!0;return!1}str=function(a){this.init(a)};str.format=function(a){var e=arguments,d=1;2==e.length&&"object"==typeof e[1]&&(e=e[1]);return a.replace(/%?%(?:\(([^\)]+)\))?([disr])/g,
function(a,b,c){if(a[0]==a[1])return a.substring(1);b=e[b||d++];return"undefined"===typeof b?a:"i"==c||"d"==c?+b:b})};str.prototype={init:function(a){this.str=a},format:function(){return str.format(this.str)},toString:function(){return this.str}};c.md5=function(a,e,d){return!e?d?B(a):C(B(a)):d?t(unescape(encodeURIComponent(e)),unescape(encodeURIComponent(a))):C(t(unescape(encodeURIComponent(e)),unescape(encodeURIComponent(a))))};var y={url:"//gravatar.com/avatar/%(md5)s?r=%(rate)s&s=%(size)s&d=%(default)s&%(forcedefault)s",
defaults:{rate:"pg",size:48,"default":encodeURIComponent("images/avatar_default_collaborator.png"),forcedefault:"",key:"Avatar",needle:"Person.EMail"},parse:function(a,e){if(a){e||(e=this.defaults.needle);var d=this,b=e.split("."),n=b[0],h=b[1];c.each(a,function(a,b){a===n&&(void 0!==h&&c.isDefined(b[h]))&&(this[d.defaults.key]=d.get(b[h]));(c.isObject(b)||c.isArray(b))&&d.parse(b,e)});return a}},get:function(a){return"string"!==c.type(a)?a:str.format(this.url,c.extend({},this.defaults,{md5:c.md5(c.trim(a.toLowerCase()))}))}};
c.avatar=y;var v,Q=/d{1,4}|m{1,4}|yy(?:yy)?|([HhMsTt])\1?|[LloSZ]|"[^"]*"|'[^']*'/g,R=/\b(?:[PMCEA][SDP]T|(?:Pacific|Mountain|Central|Eastern|Atlantic) (?:Standard|Daylight|Prevailing) Time|(?:GMT|UTC)(?:[-+]\d{4})?)\b/g,S=/[^-+\dA-Z]/g,x=function(a,e){a=String(a);for(e=e||2;a.length<e;)a="0"+a;return a};v=function(a,e,d){1==arguments.length&&("[object String]"==Object.prototype.toString.call(a)&&!/\d/.test(a))&&(e=a,a=void 0);a=a?new Date(a):new Date;if(isNaN(a))throw SyntaxError("invalid date");
e=String(v.masks[e]||e||v.masks["default"]);"UTC:"==e.slice(0,4)&&(e=e.slice(4),d=!0);var b=d?"getUTC":"get",c=a[b+"Date"](),n=a[b+"Day"](),h=a[b+"Month"](),g=a[b+"FullYear"](),f=a[b+"Hours"](),j=a[b+"Minutes"](),k=a[b+"Seconds"](),b=a[b+"Milliseconds"](),l=d?0:a.getTimezoneOffset(),m={d:c,dd:x(c),ddd:v.i18n.dayNames[n],dddd:v.i18n.dayNames[n+7],m:h+1,mm:x(h+1),mmm:v.i18n.monthNames[h],mmmm:v.i18n.monthNames[h+12],yy:String(g).slice(2),yyyy:g,h:f%12||12,hh:x(f%12||12),H:f,HH:x(f),M:j,MM:x(j),s:k,
ss:x(k),l:x(b,3),L:x(99<b?Math.round(b/10):b),t:12>f?"a":"p",tt:12>f?"am":"pm",T:12>f?"A":"P",TT:12>f?"AM":"PM",Z:d?"UTC":(String(a).match(R)||[""]).pop().replace(S,""),o:(0<l?"-":"+")+x(100*Math.floor(Math.abs(l)/60)+Math.abs(l)%60,4),S:["th","st","nd","rd"][3<c%10?0:(10!=c%100-c%10)*c%10]};return e.replace(Q,function(a){return a in m?m[a]:a.slice(1,a.length-1)})};v.masks={"default":"ddd mmm dd yyyy HH:MM:ss",shortDate:"m/d/yy",mediumDate:"mmm d, yyyy",longDate:"mmmm d, yyyy",fullDate:"dddd, mmmm d, yyyy",
shortTime:"h:MM TT",mediumTime:"h:MM:ss TT",longTime:"h:MM:ss TT Z",isoDate:"yyyy-mm-dd",isoTime:"HH:MM:ss",isoDateTime:"yyyy-mm-dd'T'HH:MM:ss",isoUtcDateTime:"UTC:yyyy-mm-dd'T'HH:MM:ss'Z'"};v.i18n={dayNames:"Sun Mon Tue Wed Thu Fri Sat Sunday Monday Tuesday Wednesday Thursday Friday Saturday".split(" "),monthNames:"Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec January February March April May June July August September October November December".split(" ")};window.livedesk.i18n&&void 0!==window.livedesk.i18n.day_names&&
(v.i18n.dayNames=window.livedesk.i18n.day_names);window.livedesk.i18n&&void 0!==window.livedesk.i18n.month_names&&(v.i18n.monthNames=window.livedesk.i18n.month_names);Date.prototype.format=function(a,e){return v(this,a,e)};Array.isArray||(Array.isArray=function(a){return"[object Array]"===Object.prototype.toString.call(a)});Function.prototype.bind||(Function.prototype.bind=function(a){if("function"!==typeof this)throw new TypeError("Function.prototype.bind - what is trying to be bound is not callable");
var e=Array.prototype.slice.call(arguments,1),d=this,b=function(){},c=function(){return d.apply(this instanceof b?this:a,e.concat(Array.prototype.slice.call(arguments)))};b.prototype=this.prototype;c.prototype=new b;return c});String.prototype.trim||(String.prototype.trim=function(){for(var a=this.replace(/^\s\s*/,""),e=/\s/,d=a.length;e.test(a.charAt(--d)););return a.slice(0,d+1)});var I=!1;this.Class=function(){};Class.extend=function(a,e){function d(){if(!I&&(this._constructor||this._construct))try{return(this._construct||
this._constructor).apply(this,arguments)}catch(a){}}I=!0;var b=new this;I=!1;for(var c in a)b[c]=a[c];d.prototype=b;d.prototype.constructor=d;d.extend=arguments.callee;return d};var K=function(){},u=function(){},L=function(){this.items={}},w=function(){},M=Class.extend({_construct:function(a){this.data=!this.data?{root:""}:this.data;switch(c.type(a)){case "string":this.data.url=a;break;case "array":this.data.url=a[0];void 0!==a[1]&&(this.data.xfilter=url[0]);break;case "object":this.data.url=a.url,
void 0!==a.xfilter&&(this.data.xfilter=a.xfilter)}return this},xfilter:function(){this.data.xfilter=1<arguments.length?c.makeArray(arguments).join(","):c.isArray(arguments[0])?arguments[0].join(","):arguments[0];return this},root:function(a){this.data.root=a;return this},get:function(){return this.data.root+this.data.url},order:function(a,e){this.data.order=e+"="+a;return this},filter:function(a,e){this.data.filter=a+"="+e;return this},decorate:function(a){this.data.url=a.replace(/(%s)/g,this.data.url)},
options:function(){var a={};this.data.xfilter&&(a.headers={"X-Filter":this.data.xfilter});return a}}),z={request:function(a){var e=this,d=function(d,b,n){c.support.cors=!0;a instanceof M?(b=c.extend(!0,{},b,e.options,n,{data:d},a.options()),d=c.ajax(e.href(a.get()),b)):(b=c.extend(!0,{},b,e.options,n,{data:d}),d=c.ajax(e.href(a),b));e.reset();b.fail&&d.fail(b.fail);b.done&&d.done(b.done);b.always&&d.always(b.always);return d};return{read:function(a){return d({},e.readOptions,a)},update:function(a,
b){return d(a,e.updateOptions,b)},insert:function(a,b){return d(a,e.insertOptions,b)},remove:function(a){return d({},e.removeOptions,a)}}},href:function(a){return a},reset:c.noop,options:{},readOptions:{dataType:"json",type:"get",headers:{Accept:"text/json"}},updateOptions:{type:"post",headers:{"X-HTTP-Method-Override":"PUT"}},insertOptions:{dataType:"json",type:"post"},removeOptions:{type:"get",headers:{"X-HTTP-Method-Override":"DELETE"}}},T=0;u.prototype={_changed:!1,_new:!1,defaults:{},data:{},
_construct:function(a,b){this._clientId=T++;this.data={};this.parseHash(a);this._new=!0;var d=this.pushUnique?this.pushUnique():this;d._forDelete=!1;d.clearChangeset();d._clientHash=null;b&&"object"==typeof b&&c.extend(d,b);"object"==typeof a&&(d._parse(a),d._setExpiration());c.isEmptyObject(d.changeset)||(d.triggerHandler("update",d.changeset),d.clearChangeset());return d},syncAdapter:z,feed:function(a,b,d){var a={},d=d?d:this.data,c;for(c in d)a[c]=d[c]instanceof u?b?d[c].feed(b):d[c].relationHash()||
d[c].hash():d[c];return a},sync:function(a,b){var d=this,n=c.Deferred(),h=function(){return d.syncAdapter.request.apply(d.syncAdapter,arguments)};this.hash();d.triggerHandler("sync");if(this._forDelete)return h(a||this.href).remove().done(function(){d._remove()});if(this._clientHash)return h(a||this.href).insert(this.feed()).done(function(a){d._changed=!1;d._parse(a);d._uniq&&d._uniq.replace(d._clientHash,d.hash(),d);d._clientHash=null;d.triggerHandler("insert").Class.triggerHandler("insert",d)});
this._changed?c.isEmptyObject(this.changeset)||(n=this.href&&h(this.href).update(b?this.feed():this.feed("json",!1,this.changeset)).done(function(){d.triggerHandler("update",d.changeset).clearChangeset()})):(!a||!a.force)&&this.exTime&&this.exTime>new Date?d.isDeleted()||d.triggerHandler("update"):n=this.href&&h(this.href).read(a).done(function(a){d._parse(a);d.isDeleted()?d._remove():c.isEmptyObject(d.changeset)?d.clearChangeset().triggerHandler("read"):d.triggerHandler("update",d.changeset).clearChangeset()});
this._setExpiration();return n},_setExpiration:function(){this.exTime=new Date;this.exTime.setSeconds(this.exTime.getSeconds()+5)},_remove:function(){this.triggerHandler("delete");this._uniq&&this._uniq.remove(this.hash())},remove:function(){this._forDelete=!0;return this},isDeleted:function(){return this._forDelete},modelDataBuild:function(a){return a},parse:function(a){return a},_parse:function(a){a=a instanceof u?a.data:this.parse(a);if(!a._parsed){for(var b in a){if(this.defaults[b])switch(!0){case "function"===
typeof this.defaults[b]&&void 0===this.data[b]:var d=this.modelDataBuild(new this.defaults[b](a[b]));!this._new&&(d!=this.data[b]&&!(d instanceof w))&&(this.changeset[b]=d);this.data[b]=d;!a[b].href&&this.data[b].relationHash&&this.data[b].relationHash(a[b]);continue;case c.isArray(this.defaults[b]):this.data[b]=this.modelDataBuild(new w(this.defaults[b][0],a[b].href));delete this.data[b];continue;case this.defaults[b]instanceof w:case this.defaults[b]instanceof u:this.data[b]=this.defaults[b];continue}else this._new||
("object"===c.type(a[b])?s(this.data[b],a[b])&&(this.changeset[b]=a[b]):this.data[b]!=a[b]&&(this.changeset[b]=a[b]));"object"===c.type(a[b])&&"object"===c.type(this.data[b])?c.extend(!0,this.data[b],a[b]):this.data[b]=a[b]}this._new=!1;a._parsed=!0}},parseHash:function(a){if(a instanceof u)return this;"string"==typeof a?this.href=a:a&&void 0!==a.href?(this.href=a.href,delete a.href):a&&(void 0!==a.id&&void 0!==this.url)&&(this.href=this.url+a.id);return this},clearChangeset:function(){this._changed=
!1;this.changeset={};return this},get:function(a){return this.data[a]},set:function(a,b,d){var n={};"string"===c.type(a)?n[a]=b:(n=a,d=b);d=c.extend({},{silent:!1},d);this.clearChangeset()._parse(n);this._changed=!0;c.isEmptyObject(this.changeset)||d.silent||this.triggerHandler("set",this.changeset);return this},_getClientHash:function(){this._clientHash||(this._clientHash="mcid-"+String(this._clientId));return this._clientHash},hash:function(){!this.href&&this.data.href&&(this.href=this.data.href);
return this.data.href||this.href||this._getClientHash()},relationHash:function(a){a&&(this.data.Id=a);return this.data.Id},off:function(a,b){c(this).off(a,b);return this},on:function(a,b,d){if(void 0===d)c(this).off(a,b),c(this).on(a,b);else c(this).on(a,function(){b.apply(d,arguments)});return this},trigger:function(a,b){c(this).trigger(a,b);return this},triggerHandler:function(a,b){c(this).triggerHandler(a,b);return this}};L.prototype={items:{},garbageTime:1500,refresh:function(a){a._exTime||(a._exTime=
new Date);a._exTime.setTime(a._exTime.getTime()+this.garbageTime)},set:function(a,b){var d=this;c(b).on("sync get get-prop set-prop",function(){d.refresh(this)});d.refresh(b);this.items[a]||(this.items[a]=b);return this.items[a]},replace:function(a,b,d){delete this.items[a];return this.set(b,d)},garbage:function(){for(var a in this.items)this.items[a]._exTime&&this.items[a]._exTime<new Date&&(c(this.items[a]).triggerHandler("garbage"),delete this.items[a])},remove:function(a){delete this.items[a]}};
var D=u.options={},N,O;u.extend=N=function(a,b){var d;d=Class.extend.call(this,a);d.extend=N;d.prototype.Class=d;d.on=function(a,b,e){c(d).on(a,function(){b.apply(e,arguments)});return d};d.off=function(a,b){c(d).off(a,b);return d};d.triggerHandler=function(a,b){c(d).triggerHandler(a,b)};b&&b.register&&(K[b.register]=d,delete b.register);d.prototype.options=c.extend({},b);return d};w.prototype={_list:[],getList:function(){return this._list},count:function(){return this._list.length},_construct:function(){this.model||
(this.model=u);this._list=[];this.desynced=!0;var a=buildOptions=function(){void 0},b;for(b in arguments)switch(c.type(arguments[b])){case "function":this.model=arguments[b];break;case "string":this.href=arguments[b];break;case "array":a=function(a){return function(){this._list=this._parse(a)}}(arguments[b]);break;case "object":buildOptions=function(a){return function(){this.options=a;a.href&&(this.href=a.href)}}(arguments[b])}buildOptions.call(this);a.call(this);D=c.extend({},{init:!0},this.options);
D.init&&this.init.apply(this,arguments)},init:function(){},get:function(a){var b=c.Deferred(),d=this;searchKey=function(){for(var c=0;c<d._list.length;c++)if(a==d._list[c].hash()||a==d._list[c].relationHash())return b.resolve(d._list[c]);b.reject()};this.desynced&&this.sync().done(function(){b.resolve(searchKey())})?b:searchKey();return b},remove:function(a){for(var b in this._list)if(a==this._list[b].hash()||a==this._list[b].relationHash()){Array.prototype.splice.call(this._list,b,1);break}return this},
syncAdapter:z,setHref:function(a){this.href=a;return this},each:function(a){c.each(this._list,a)},forwardEach:function(a,b){this._list.forEach(a,b)},reverseEach:function(a,b){for(var d=this._list.length;0<d;++d)a.call(b||this,this[d],d,this)},feed:function(a,b){var d=[],c;for(c in this._list)d[c]=this._list[c].feed(a,b);return d},sync:function(a){var b=this;return this.href&&this.syncAdapter.request.call(this.syncAdapter,this.href).read(a).done(function(a){for(var a=b._parse(a),c=[],n=[],h=b._list.length,
l=0;l<a.length;l++){for(var g=!1,f=0;f<h;f++)if(a[l].hash()==b._list[f].hash()){g=a[l];break}if(g)if(n.push(g),g.isDeleted())g._remove();else g.on("delete",function(){b.remove(this.hash())}).on("garbage",function(){this.desynced=!0});else a[l].isDeleted()?n.push(a[l]):(b._list.push(a[l]),c.push(a[l]))}b.desynced=!1;0===h?b.triggerHandler("read"):(b.triggerHandler("updates",[n]),b.triggerHandler("addings",[c]))})},modelDataBuild:function(a){return a},parse:function(a){var b=a;if(!Array.isArray(a))for(i in a)if(c.isArray(a[i])){b=
a[i];break}return b},_parse:function(a){if(a._parsed)return a._parsed;var a=this.parse(a),b,d=[],c;for(b in a)a.hasOwnProperty(b)&&(c=new this.model(a[b]),c=this.modelDataBuild(c),d.push(c));a._parsed=d;return a._parsed},insert:function(a){this.desynced=!1;a instanceof u||(a=this.modelDataBuild(new this.model(a)));this._list.push(a);a.hash();return a.sync(this.href)},off:function(a,b){c(this).off(a,b);return this},on:function(a,b,d){if(void 0===d)c(this).off(a,b),c(this).on(a,b);else c(this).on(a,
function(){b.apply(d,arguments)});return this},trigger:function(a,b){c(this).trigger(a,b);return this},triggerHandler:function(a,b){c(this).triggerHandler(a,b);return this}};w.extend=O=function(a){a=Class.extend.call(this,a);a.extend=O;D&&D.register&&(w[D.register]=a);return a};var U=0,y=Class.extend({getProperty:function(a){return!this[a]?null:"function"===typeof this[a]?this[a]():this[a]}}).extend({tagName:"div",attributes:{className:"",id:""},namespace:"view",_constructor:function(a,b){c.extend(this,
a);this._clientId=U++;b=c.extend({},{init:!0,events:!0,ensure:!0},b);b.ensure&&this._ensureElement();b.init&&this.init.apply(this,arguments);b.events&&this.resetEvents()},_ensureElement:function(){var a=this.attributes.className,b=this.attributes.id,d="";c(this.el).length?this.el=c(this.el):("string"===c.type(this.el)&&("."==this.el[0]&&(a+=this.el.substr(0,1)),"#"==this.el[0]&&(b=this.el.substr(0,1))),d="<"+this.tagName,""!==a&&(d=d+' class="'+a+'"'),""!==b&&(d=d+' id="'+b+'"'),d=d+"></"+this.tagName+
">",this.el=c(d))},init:function(){return this},resetEvents:function(){this.undelegateEvents();this.delegateEvents()},delegateEvents:function(a){if(a||(a=this.getProperty("events")))for(var b in a){var d=a[b],n;for(n in d){var h=d[n];if("string"===typeof h&&c.isFunction(this[h]))c(this.el).on(this.getEvent(n),b,this[h].bind(this))}}},undelegateEvents:function(){c(this.el).off(this.getNamespace());return this},getEvent:function(a){return a+this.getNamespace()},getNamespace:function(){return"."+this.getProperty("namespace")},
render:function(){this.delegateEvents();return this},remove:function(){c(this.el).remove();this.destroy();return this},destroy:function(){this.model&&this.model.trigger("destroy");this.collection&&this.collection.trigger("destroy");return this},checkElement:function(){return void 0===this.el?!1:void 0!==this.el.selector&&""!=this.el.selector?1===c(this.el.selector).length:c(this.el).is(":visible")},setElement:function(a){this.undelegateEvents();var a=c(a),b=this.el.data();this.el.replaceWith(a);this.el=
a;this.el.data(b);this.delegateEvents();return this},resetElement:function(a){this.el=c(a);this._ensureElement();this.delegateEvents()}}),P=u,J=w,z=c.extend({},z,{reset:function(){try{delete this.options.headers["X-Filter"],delete this.options.data["CId.since"],delete this.options.data.offset,delete this.options.data.limit}catch(a){}}}),V=function(){var a=this;AuthApp.success=function(){a.options.headers.Authorization=localStorage.getItem("superdesk.login.session")};AuthApp.require.apply(a,arguments)},
E=c.extend({},z,{options:{headers:{Authorization:localStorage.getItem("superdesk.login.session")},fail:function(a){401==a.status&&V.apply(E,arguments);404==a.status&&ErrorApp.require.apply(this,arguments)}},href:function(a){return-1===a.indexOf("my/")?a.replace("resources/","resources/my/"):a}}),F=function(){this.syncAdapter.options.headers||(this.syncAdapter.options.headers={});this._xfilter=1<arguments.length?c.makeArray(arguments).join(","):c.isArray(arguments[0])?arguments[0].join(","):arguments[0];
this.syncAdapter.options.headers["X-Filter"]=this._xfilter;this.syncAdapter.options.headers["X-Format-DateTime"]="M/dd/yyyy HH:mm:ss";return this},G=function(a){a?c.extend(!0,this.syncAdapter.options,{data:{"CId.since":a}}):delete this.syncAdapter.options.data["CId.since"];return this},u=P.extend({isDeleted:function(){return this._forDelete||this.data.DeletedOn},syncAdapter:z,xfilter:F,since:G}),W=u.extend({syncAdapter:E,xfilter:F,since:G}),w=J.extend({xfilter:F,since:G,asc:function(a){c.extend(!0,
this.syncAdapter.options,{data:{asc:a}});return this},desc:function(a){c.extend(!0,this.syncAdapter.options,{data:{desc:a}});return this},limit:function(a){c.extend(!0,this.syncAdapter.options,{data:{limit:a}});return this},offset:function(a){c.extend(!0,this.syncAdapter.options,{data:{offset:a}});return this},syncAdapter:z}),J=w.extend({xfilter:F,since:G,syncAdapter:E});u.extend=function(){var a=P.extend.apply(this,arguments),b=new L;c.extend(a.prototype,{_uniq:b,pushUnique:function(){return b.set(this.hash(),
this)}},arguments[0]);return a};c.gizmo={Model:u,AuthModel:W,Collection:w,AuthCollection:J,Sync:z,AuthSync:E,View:y,Url:M,Register:K};r.preLoad(m)})(jQuery)};function isOnly(m,r){"string"===$.type(r)&&(r=[r]);var c=0,p=r.length;for(i in m){if(-1===$.inArray(i,r))return!1;c++;if(c>p)return!1}return c===p}var root=this;
window.livedesk.loadXDRequest=function(m){var r=m;root.XDomainRequest&&r.ajaxTransport("+*",function(c){if(c.crossDomain&&c.async){c.timeout&&(c.xdrTimeout=c.timeout,delete c.timeout);var m;return{send:function(q,b){function n(c,n,h,t){m.onload=m.onerror=m.ontimeout=r.noop;m=void 0;b(c,n,h,t)}m=new XDomainRequest;if(c.dataType){var h="";for(i in c.headers)h+=i+"="+encodeURIComponent(c.headers[i])+"&";h=h.replace(/(\s+)?.$/,"");c.url=c.url+(-1===c.url.indexOf("?")?"?":"&")+h}m.open(c.type,c.url);m.onload=
function(){n(200,"OK",{text:m.responseText},"Content-Type: "+m.contentType)};m.onerror=function(){n(404,"Not Found")};c.xdrTimeout&&(m.ontimeout=function(){n(0,"timeout")},m.timeout=c.xdrTimeout);m.send(c.hasContent&&c.data||null)},abort:function(){m&&(m.onerror=r.noop(),m.abort())}}}})};
window.livedesk.init=function(){window.livedesk.location=window.location.href.split("#")[0];var m=this,r=!1,c=!1;contentPath=void 0===m.contentPath?"":m.contentPath;"undefined"==typeof jQuery?r=!0:1.7>parseFloat($().jquery)&&(c=r=!0);r?m.loadScript("//ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js",function(){m.loadXDRequest(jQuery);"undefined"==typeof $.gizmo?m.loadGizmo(c):m.preLoad(c)}):(m.loadXDRequest(jQuery),"undefined"==typeof $.gizmo?m.loadGizmo(c):m.preLoad(c))};
window.livedesk.loadScript=function(m,r){var c=document.createElement("script");c.type="text/javascript";c.readyState?c.onreadystatechange=function(){if("loaded"==c.readyState||"complete"==c.readyState)c.onreadystatechange=null,r()}:c.onload=function(){r()};c.src=m;document.getElementsByTagName("head")[0].appendChild(c)};window.livedesk.preLoad=function(m){m?(m=$.noConflict(!0),this.startLoading(m,window.livedesk._)):this.startLoading(jQuery,window.livedesk._)};
window.livedesk.startLoading=function(m,r){var c=m.gizmo.Model.extend({}),c=m.gizmo.Model.extend({defaults:{Creator:c},services:{flickr:!0,google:!0,twitter:!0,facebook:!0,youtube:!0},getClass:function(){switch(this.get("Type").Key){case "wrapup":return"wrapup";case "quote":return"quotation";case "advertisement":return"advertisement";default:return this.isService()?"service":"tw"}},isService:function(){return this.get("AuthorName")in this.services},isQuote:function(){return"quotation"==this.getClass()},
twitter:{link:{anchor:function(b){return b.replace(/[A-Za-z]+:\/\/[A-Za-z0-9-_]+\.[A-Za-z0-9-_:%&\?\/.=]+/g,function(b){b=b.link(b);return b=b.replace('href="','target="_blank" href="')})},user:function(b){return b.replace(/[@]+[A-Za-z0-9-_]+/g,function(b){var c=b.replace("@",""),b=b.link("http://twitter.com/"+c);return b=b.replace('href="','target="_blank" onclick="loadProfile(\''+c+'\');return(false);"  href="')})},tag:function(b){return b.replace(/[#]+[A-Za-z0-9-_]+/g,function(b){var c=b.replace(" #",
" %23"),b=b.link("http://summize.com/search?q="+c);return b=b.replace('href="','target="_blank" href="')})},all:function(b){b=this.anchor(b);b=this.user(b);return b=this.tag(b)}}}});Posts=m.gizmo.Collection.extend({timeInterval:1E4,idInterval:0,_latestCId:0,keep:!1,init:function(){var b=this;this.on("readauto updates",function(c,h){void 0===h&&(h=b._list);b.getMaximumCid(h)})},destroy:function(){this.stop()},auto:function(){var b=this;ret=this.stop().start();this.idInterval=setInterval(function(){b.start()},
this.timeInterval);return ret},getMaximumCid:function(b){p=0;for(count=b.length;p<count;p++){var c=parseInt(b[p].get("CId"));!isNaN(c)&&this._latestCId<c&&(this._latestCId=c)}},start:function(){var b={data:{"cId.since":this._latestCId},headers:{"X-Filter":this._xfilter,"X-Format-DateTime":"M/dd/yyyy HH:mm:ss"}};0===this._latestCId&&delete b.data;if(!this.keep&&this.view&&!this.view.checkElement())this.stop();else return this.triggerHandler("beforeUpdate"),this.autosync(b)},stop:function(){clearInterval(this.idInterval);
return this},autosync:function(b){var c=this;return this.href&&this.syncAdapter.request.call(this.syncAdapter,this.href).read(b).done(function(b){for(var b=c._parse(b),m=[],l=[],r=c._list.length,t=0;t<b.length;t++){for(var p=!1,q=0;q<r;q++)if(b[t].hash()==c._list[q].hash()){p=b[t];break}if(p)if(l.push(p),p.isDeleted())p._remove();else p.on("delete",function(){c.remove(this.hash())}).on("garbage",function(){this.desynced=!0});else b[t].isDeleted()?l.push(b[t]):(c._list.push(b[t]),m.push(b[t]))}c.desynced=
!1;0===r?c.triggerHandler("readauto"):(c.triggerHandler("updatesauto",[l]),c.triggerHandler("addingsauto",[m]))})}}).extend({parse:function(b){void 0!==b.total&&(b.total=parseInt(b.total),void 0===this.total&&(this.total=b.total),delete b.total);return b.PostList?b.PostList:b},model:c});Blog=m.gizmo.Model.extend({defaults:{PostPublished:Posts}});var p=0,q;q=m.gizmo.View.extend({init:function(){var b=this;b.xfilter="PublishedOn, DeletedOn, Order, Id, CId, Content, CreatedOn, Type, AuthorName, Author.Source.Name, Author.Source.Id, IsModified, AuthorPerson.EMail, AuthorPerson.FirstName, AuthorPerson.LastName, AuthorPerson.Id, Meta";
b.model.on("read update",function(c,h){b.render(c,h)}).on("delete",b.remove,b).xfilter(b.xfilter).sync()},remove:function(){this._parent.removeOne(this);this.el.remove();return this},itemTemplate:function(b,c,h,m){var l="",p=b.getClass(),q=b.get("AuthorName"),C="",B="";if(b.data.hasOwnProperty("Meta")){var s=b.data.Meta;"string"==typeof s&&(s=JSON.parse(s));s.hasOwnProperty("annotation")&&("string"===typeof s.annotation?B='<div class="editable annotation">'+s.annotation+"</div>":null!==s.annotation[1]?
(C='<div class="editable annotation">'+s.annotation[0]+"</div>",B='<div class="editable annotation">'+s.annotation[1]+"</div>"):B='<div class="editable annotation">'+s.annotation[0]+"</div>")}avatarString="";"true"!=r("no_avatar")&&(0<m.length&&"twitter"!=q)&&(avatarString='<figure><img src="'+m+'" ></figure>');switch(p){case "tw":case "service":l=l+C+avatarString;l+='<div class="result-content">';"twitter"==q?(l+='<blockquote class="twitter-tweet"><p>'+c+"</p>&mdash; "+s.from_user_name+" (@"+s.from_user_name+
') <a href="https://twitter.com/'+s.from_user+"/status/"+s.id_str+'" data-datetime="'+s.created_at+'"></a></blockquote>',window.livedesk.loadedTweeterScript||(window.livedesk.loadScript("//platform.twitter.com/widgets.js",function(){}),window.livedesk.loadedTweeterScript=!0)):"youtube"==q?(l+='<div class="result-text">'+c+"</div>",l+='<p class="attributes"><i class="source-icon"></i> '+r("by")+" ",l+='<a class="author-name" href="http://youtube.com/'+s.uploader+'" target="_blank">'+s.uploader+"</a>"):
"google"==q?(l+='<h3><a target="_blank" href="'+s.unescapedUrl+'">'+s.title+"</a></h3>",l+='<div class="result-text">'+c+"</div>",l+='<p class="attributes"><i class="source-icon"></i> '+r("by")+" "+b.get("AuthorName")):"flickr"==q?(l+='<div class="result-text">'+c+"</div>",l+='<p class="attributes"><i class="source-icon"></i> '+r("by")+" "+b.get("AuthorName")):(l+='<div class="result-text">'+c+"</div>",l+='<p class="attributes"><i class="source-icon"></i> '+r("by")+" "+b.get("AuthorName"),l+="<time>"+
h+"</time>");l+="</p>";l+="</div>";l+=B;break;case "quotation":var y,b=b.get("AuthorName"),h=c.split("<div><br><br></div>"),m=c.split("<br><br><br>");2==h.length?(c=h[0],y='<div class="quotation-author">'+h[1]+"</div>"):2==m.length&&(c=m[0],y='<div class="quotation-author">'+m[1]+"</div>");l+='<div class="result-content">';l+='<div class="result-text">'+c+"</div>";l=y?l+y:l+('<div class="attributes">'+r("by")+" "+b+"</div>");l+="</div>";break;case "wrapup":l+='<span class="big-toggle"></span>';l+=
"<h3>"+c+"</h3>";break;case "advertisement":l+=c}return l},toggleWrap:function(b,c){"boolean"!=typeof c&&(c=!1);this._toggleWrap(m(b).closest("li").first(),c)},_toggleWrap:function(b,c){"boolean"!=typeof c&&(c=!1);if(b.hasClass("open")){var h=!0,r=window.location.hash;0<r.length&&!1==c&&b.nextUntil(".wrapup").each(function(){"#"+m(this).find("a").attr("name")==r&&(h=!1)});h&&(b.removeClass("open").addClass("closed"),b.nextUntil(".wrapup").hide())}else b.removeClass("closed").addClass("open"),b.nextUntil(".wrapup").show()},
togglePermalink:function(b){this._togglePermalink(m(b).next('input[data-type="permalink"]'))},_togglePermalink:function(b){"visible"==b.css("visibility")?b.css("visibility","hidden"):b.css("visibility","visible")},render:function(){countLoaded++;var b=this,c=parseFloat(b.model.get("Order")),h="";this.model.get("AuthorPerson")&&this.model.get("AuthorPerson").EMail&&(h=m.avatar.get(b.model.get("AuthorPerson").EMail));!isNaN(b.order)&&c!=b.order&&(b.order=c,b._parent.reorderOne(b));var p=b.model.get("Content"),
c="";"wrapup"==b.model.getClass()&&(c+="open ");if(b.model.isService()){var c=c+b.model.get("AuthorName"),l=JSON.parse(b.model.get("Meta")),q=b.model.get("PublishedOn"),q=new Date(q),t=q.format("ddd mmm dd yyyy HH:MM:ss TT");"flickr"==b.model.get("AuthorName")?(p=m("<span>"+p+"</span>"),p.find("img").attr("src",p.find("a").attr("href")),p=p.html()):"twitter"==b.model.get("AuthorName")?(h=l.profile_image_url,p=b.model.twitter.link.all(p)):"google"==b.model.get("AuthorName")&&l.tbUrl&&(p+='<p><a href="'+
l.url+'"><img src="'+l.tbUrl+'" height="'+l.tbHeight+'" width="'+l.tbWidth+'"></a></p>')}q=b.model.get("PublishedOn");q=new Date(q);t=q.format(r("ddd mmm dd yyyy HH:MM:ss TT"));"true"===r("show_current_date")&&(new Date).format("mm dd yyyy")==q.format("mm dd yyyy")&&(t=q.format(r("HH:MM:ss TT")));b.model.get("AuthorName");p=b.itemTemplate(b.model,p,t,h);l=b.model.get("Id");h=b._parent.model.get("Title");h=h.replace(/ /g,"-");h=l+"-"+encodeURI(h);h=l;l=b.model.getClass();q=window.livedesk.location+
"#"+h;t="";"advertisement"!==l&&"wrapup"!==l&&(t='<a rel="bookmark" href="#'+h+'">#</a><input type="text" value="'+q+'" style="visibility:hidden" data-type="permalink" />');c='<li class="'+c+l+'"><a name="'+h+'"></a>'+p+"&nbsp;"+t+"</li>";"undefined"!=typeof window.livedesk.productionServer&&"undefined"!=typeof window.livedesk.frontendServer&&(re=RegExp(window.livedesk.productionServer,"g"),c=c.replace(re,window.livedesk.frontendServer));b.setElement(c);b.model.triggerHandler("rendered");m(b.el).off("click.livedesk",
".big-toggle").on("click.livedesk",".big-toggle",function(){b.toggleWrap(this,!0)});m(b.el).off("click.livedesk",'a[rel="bookmark"]').on("click.livedesk",'a[rel="bookmark"]',function(){b.togglePermalink(this)});m(b.el).off("click.livedesk",'input[data-type="permalink"]').on("focus.livedesk click.livedesk",'input[data-type="permalink"]',function(){m(this).select()})}});countLoaded=iidLoadTrace=totalLoad=0;c=m.gizmo.View.extend({limit:5,offset:0,el:"#livedesk-root",timeInterval:1E4,idInterval:0,_latestCId:0,
events:{"#liveblog-more":{click:"more"}},more:function(b){var c=this;c.model.get("PostPublished");c.model.get("PostPublished").xfilter(c.xfilter).limit(c.limit).offset(c._views.length).sync().done(function(){var h=c.model.get("PostPublished").total;c._views.length>=h&&m(b.target).hide()})},setIdInterval:function(b){this.idInterval=setInterval(b,this.timeInterval);return this},pause:function(){clearInterval(this.idInterval);return this},sync:function(){var b=this;this.auto().pause().setIdInterval(function(){b.auto()})},
auto:function(){this.model.xfilter().sync({force:!0});return this},ensureStatus:function(){if(this.model.get("ClosedOn")){var b=new Date(this.model.get("ClosedOn"));this.pause();this.model.get("PostPublished").pause();this.el.find("#liveblog-status").html(r("The liveblog coverage was stopped ")+b.format(r("mm/dd/yyyy HH:MM:ss")))}},gotoHash:function(){if(0<location.hash.length){var b=location.hash;location.hash="";location.hash=b}},init:function(){var b=this;b._views=[];b.rendered=!1;"string"===m.type(b.url)&&
(b.model=new Blog(b.url.replace("my/","")));b.xfilter="PublishedOn, DeletedOn, Order, Id, CId, Content, CreatedOn, Type, AuthorName, Author.Source.Name, Author.Source.Id, IsModified, AuthorPerson.EMail, AuthorPerson.FirstName, AuthorPerson.LastName, AuthorPerson.Id, Meta";b.model.on("read",function(){b.rendered||b.model.get("PostPublished").on("read readauto",b.render,b).on("addings addingsauto",b.addAll,b).on("addingsauto",b.updateTotal,b).on("updates updatesauto",b.updateStatus,b).on("beforeUpdate",
b.updateingStatus,b).limit(b.limit).offset(b.offset).xfilter(b.xfilter).auto();b.rendered=!0}).on("update",function(){b.ensureStatus();b.renderBlog()});b.sync()},removeOne:function(b){b=this._views.indexOf(b);this.model.get("PostPublished").total--;this._views.splice(b,1);return this},reorderOne:function(b){this._views.sort(function(b,c){return b.order-c.order});pos=this._views.indexOf(b);0===pos?b.el.insertAfter(this._views[1].el):b.el.insertBefore(this._views[0<pos?pos-1:1].el)},addOne:function(b){var c=
new q({model:b,_parent:this}),h=this._views.length;b.postview=c;c.order=parseFloat(b.get("Order"));if(h){var m,l;for(p=0;p<h;p++)if(c.order>this._views[p].order)m=this._views[p],nextIndex=p;else if(c.order<this._views[p].order){l=this._views[p];prevIndex=p;break}l?(c.el.insertAfter(l.el),this._views.splice(prevIndex,0,c)):m&&(c.el.insertBefore(m.el),this._views.splice(nextIndex+1,0,c))}else this.el.find("#liveblog-post-list").prepend(c.el),this._views=[c];return c},updateTotal:function(b,c){for(var h=
c.length;h--;)this.model.get("PostPublished").total++},addAll:function(b,c){for(var h=c.length;h--;)this.addOne(c[h])},updateingStatus:function(){this.el.find("#liveblog-status").html(r("updating..."))},updateStatus:function(){var b=new Date;this.el.find("#liveblog-status").fadeOut(function(){m(this).text(r("updated on ")+b.format(r("HH:MM:ss"))).fadeIn()})},renderBlog:function(){},loadTrace:function(){countLoaded>=totalLoad&&(this.gotoHash(),clearInterval(iidLoadTrace))},render:function(){var b=
this.model.get("PostPublished").total;this.el.html('<article><h2></h2><p></p></article><div class="live-blog"><p class="update-time" id="liveblog-status"></p><div id="liveblog-posts"><ol id="liveblog-post-list" class="liveblog-post-list"></ol></div><div><a id="liveblog-more" href="javascript:void(0)">'+r("More")+"</a></div>");this.limit>=b&&m("#liveblog-more",this.el).hide();this.renderBlog();this.ensureStatus();data=this.model.get("PostPublished")._list;totalLoad=b=data.length;var c=this,h;iidLoadTrace=
setInterval(function(){c.loadTrace()},900);this.views=[];for(this.renderedTotal=b;b--;)data[b].on("rendered",this.renderedOn,this),h=this.addOne(data[b]),this.views.push(h)},renderedOn:function(){this.renderedTotal--;this.renderedTotal||(this.closeAllButFirstWrapup(),this.addClassToHashItem())},closeAllButFirstWrapup:function(b){b=this.views;b.reverse();for(var c=0;c<b.length;c++)m(b[c].el).hasClass("wrapup")&&b[c]._toggleWrap(m(b[c].el))},addClassToHashItem:function(){var b=window.location.hash.split("#");
1<b.length&&m('a[name="'+b[1]+'"]').addClass("hash-open")}});window.livedesk.TimelineView=c;window.livedesk.callback()};window.livedesk.init();
