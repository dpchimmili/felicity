import moment from 'moment';


export const parseDate = function(str: any) {
    let date = moment(str);
    if(date.isValid()) {
        return date.format('MMMM Do YYYY, h:mm:ss a');
    }
    return str;
}

export const subtractDates = (first: any, second: any)  => Math.floor(Math.abs(first - second)/ (1000 * 60 * 60 * 24))

export const parseEdgeNodeToList = (payload: any) => {
    const list: any[] = [];
    if(!payload || !payload?.edges) return payload;
    payload?.edges.forEach((item: any) => list.push(item?.node));
    return list
}

export const isNullOrWs = function(str: any) {
    return (
      typeof str === "undefined" ||
      str === null ||
      (typeof str === "string" && str.trim().length === 0)
    );
  };
  
const isValidJson = function(str: any) {
    try {
        JSON.parse(str);
    } catch (e) {
        return false;
    }
    return true;
};

export const parseData = function(data: any) {
    if (!data) return {};
    if (typeof data === 'object') return data;
    if (typeof data === 'string') return JSON.parse(data);
    return {};
}

export const parseUrlParams = () => {
    const search = window.location.search.substring(1);
    if (!search) return {};

    const str = search.replace(/&/g, '","').replace(/=/g, '":"');
    const json = `{"${str}"}`;
    const transform = (key: any, value: any) =>
        isNullOrWs(key) ? value : decodeURIComponent(value);

    return isValidJson(json) ? JSON.parse(json, transform) : {};
}

export const startsWith = (str: any, word: any) => {
    return str.lastIndexOf(word, 0) === 0;
}

export function ifZeroEmpty(val: any): any {
  if(val === undefined) return "";
  return val === 0 ? '' : val;
}

export function ifNoValEmpty(val: any): any {
  if(val === undefined) return "";
  if(val === null) return "";
  if(!val) return "";
  return val;
}

export function deDuplicateArrayBy(arr: any[], key: string): any[] {
  return [...new Map(arr.map(item => [item[key], item])).values()]
}

export function addListsUnique(f: any[], s: any[], key: string): any[] {
  const c = f?.concat(s);
  return deDuplicateArrayBy(c,key);
}

export default {
    isNullOrWs,
    parseUrlParams,
    startsWith,
};


export const snakeToCamel = (val: any) => {
    const convert = (s: any) => s.replace(/(_\w)/g, (k: any) => k[1].toUpperCase());
    if (typeof val === 'object') {
        const data = Object.entries(val).reduce((x: any,[k,v]) => (x[convert(k)]=v) && x, {});
        return data;
    }
    if (typeof val === 'string') {
        return convert(val);
    }
    throw "--- error converting ---"
}

export const toCamel = (str: string) => {
    return str.replace(/([-_][a-z])/ig, ($1) => {
      return $1.toUpperCase()
        .replace('-', '')
        .replace('_', '');
    });
  };
  
export  const isObject = (obj: any) => {
    return obj === Object(obj) && !Array.isArray(obj) && typeof obj !== 'function';
};

export const keysToCamel:any = (obj: any) => {
    if (isObject(obj)) {
      const n:any = {};
  
      Object.keys(obj)
        .forEach((k) => {
          n[toCamel(k)] = keysToCamel(obj[k]);
        });
  
      return n;
    } else if (Array.isArray(obj)) {
      return obj.map((i) => {
        return keysToCamel(i);
      });
    }
    
    return obj;
};