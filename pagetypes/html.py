from common import *
from Products.ZWiki.I18n import _
from Products.ZWiki.pagetypes import registerPageType

class PageTypeHtml(PageTypeBaseHtml):
    _id = 'html'
    _name = 'HTML'
    supportsHtml = yes
    supportsDtml = yes
    supportsEpoz = yes

    def preRender(self, page, text=None):
        t = text or (page.read()+'\n'+MIDSECTIONMARKER)
        t = page.applyWikiLinkLineEscapesIn(t)
        t = page.markLinksIn(t)
        t = self.protectEmailAddresses(page,t)
        return t

    def render(self, page, REQUEST={}, RESPONSE=None, **kw):
        if page.dtmlAllowed() and page.hasDynamicContent():
            t = page.evaluatePreRenderedAsDtml(page,REQUEST,RESPONSE,**kw)
        else:
            t = page.preRendered()
        t = page.renderMarkedLinksIn(t)
        t = page.renderMidsectionIn(t,**kw)
        t = page.addSkinTo(t,**kw)
        return t

registerPageType(PageTypeHtml)

# backwards compatibility - need this here for old zodb objects
ZwikiHtmlPageType = PageTypeHtml
