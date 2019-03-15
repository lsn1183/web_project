export function generateTitle(title) {
    //$te这个方法用以判断需要翻译的key在你提供的语言包(messages)中是否存在.
    const hasKey = this.$te('route.' + title)
    const translatedTitle = this.$t('route.' + title)

    if (hasKey) {
        return translatedTitle
    }
    return title
}