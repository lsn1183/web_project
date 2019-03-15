from win32com.client import Dispatch
from win32com.client import DispatchEx
from win32com.client import constants

# xl = Dispatch('Excel.Application')
# xl.Workbooks.Open(r'C:\workspace\Spec2DB\iDesign_Task管理表.xlsx')
xl = DispatchEx('Excel.Application')
wb = xl.Workbooks.Open(r'C:\workspace\Spec2DB\iDesign_Task管理表.xlsx')
wb.SaveAs(r'c:\test_html', constants.xlHtml)
xl.Workbooks.Close()
xl.Quit()
del xl
