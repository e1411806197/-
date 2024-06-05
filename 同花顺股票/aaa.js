// 解析title中的json数据 来解析基本每股收入
function get_sy(pp){
    let obj=JSON.parse(pp)
    let res=obj['report'][7][0]
    return res
}
