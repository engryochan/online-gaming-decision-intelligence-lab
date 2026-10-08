/* Source and licensing information for the line(s) below can be found at https://live.euronext.com/modules/custom/ajax_secure/js/ajax-secure.js. */
var ajax_secure_encrypt = function(valueToEncrypt, kye) {
  // encrypt value
  let encrypted = CryptoJSAesJson.encrypt(valueToEncrypt, kye)
  //console.log('Encrypted:', encrypted)
  return encrypted;
};
var ajax_secure_decrypt = function(valueToDecrypt, kye) {
  if (typeof valueToDecrypt != 'string')
    valueToDecrypt = JSON.stringify(valueToDecrypt);

   // decrypt value
  let decrypted = CryptoJSAesJson.decrypt(valueToDecrypt, kye)
  //console.log('Decrypted:', decrypted)
  return decrypted;
};
var ajax_secure_dataFilter = function (retData, type, wantString) {
  if (drupalSettings.ajax_secure.kye != undefined) {
    var kye = drupalSettings.ajax_secure.kye;
  } else {
    var kye = '24ayqVo7yJma';
  }
  var data = [];
  var retData2 = '';
  try
  {
    if (type === 'json') {
      data = retData;
      retData2 = JSON.stringify(retData);
    } else {
      data = JSON.parse(retData);
      retData2 = retData;
    }
    if (data.ct && data.iv && data.s) {
      try
      {
        var returnn = ajax_secure_decrypt(retData2, kye);
        if (wantString===false) {
          return returnn;
        }
        return JSON.stringify(returnn);
      }
      catch(err)
      {
        console.log(err);
      }
    }
  }
  catch(err)
  {
    //console.log('IS_NOT_JSON');
  }
  return retData;
}

jQuery.ajaxSetup({
  dataFilter: function (retData, type) {
    return ajax_secure_dataFilter(retData, type);
  }
});

/* Source and licensing information for the above line(s) can be found at https://live.euronext.com/modules/custom/ajax_secure/js/ajax-secure.js. */