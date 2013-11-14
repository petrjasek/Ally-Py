# '''
# Created on May 4, 2012
# 
# @package: internationalization
# @copyright: 2012 Sourcefabric o.p.s.
# @license: http://www.gnu.org/licenses/gpl-3.0.txt
# @author: Mugur Rus
# 
# API specifications for PO file management.
# '''
# 
# from ally.api.config import service, call, model
# from ally.api.type import Reference, Scheme
# from internationalization.api.domain import modelLocalization
# from internationalization.language.api.language import Language
# 
# # --------------------------------------------------------------------
# @modelLocalization(id='Name')
# class JSONLocale:
#     '''
#     Model for a JSON locale file.
#     '''
#     Name = str
#     Locale = str
#     Reference = Reference
# 
# # --------------------------------------------------------------------
# 
# @service
# class IJSONLocaleFileService:
#     '''
#     The JSON locale service.
#     '''
# 
#     @call
#     def getGlobalJSONFile(self, locale:JSONLocale.Locale, scheme:Scheme) -> JSONLocale.Reference:
#         '''
#         Provides the messages for the whole application and the given locale in JSON format.
#         For format @see: IPOFileManager.getGlobalAsDict.
# 
#         @param locale: string
#             The locale for which to return the translation.
#         @return: string
#             The path to the temporary JSON file.
#         '''
# 
#     @call
#     def getComponentJSONFile(self, name:JSONLocale.Name, locale:JSONLocale.Locale,
#                              scheme:Scheme) -> JSONLocale.Reference:
#         '''
#         Provides the messages for the given component and the given locale in JSON format.
#         For format @see: IPOFileManager.getGlobalAsDict.
# 
#         @param component: Component.Id
#             The component for which to return the translation.
#         @param locale: string
#             The locale for which to return the translation.
#         @return: string
#             The path to the temporary JSON file.
#         '''