using OpenQA.Selenium;
using OpenQA.Selenium.Support.UI;
using System;
using System.Linq;

namespace UITests.Pages
{
  public class KhoaPage
  {
    private readonly IWebDriver _driver;
    private readonly WebDriverWait _wait;

    public KhoaPage(IWebDriver driver)
    {
      _driver = driver;
      _wait = new WebDriverWait(driver, TimeSpan.FromSeconds(10));
    }

    public void ClickAddButton()
    {
      _driver.FindElement(By.CssSelector("[data-testid='btn-them']")).Click();
    }

    public void EnterKhoa(string tenKhoa, string tenVietTat, string viTri, string moTa)
    {
      WebDriverWait wait = new WebDriverWait(_driver, TimeSpan.FromSeconds(5));
      wait.Until(driver => driver.FindElement(By.Name("tenKhoa")).Displayed);

      _driver.FindElement(By.Name("tenKhoa")).SendKeys(Keys.Control + "a");
      _driver.FindElement(By.Name("tenKhoa")).SendKeys(Keys.Delete);
      _driver.FindElement(By.Name("tenKhoa")).SendKeys(tenKhoa);

      _driver.FindElement(By.Name("tenVietTat")).SendKeys(Keys.Control + "a");
      _driver.FindElement(By.Name("tenVietTat")).SendKeys(Keys.Delete);
      _driver.FindElement(By.Name("tenVietTat")).SendKeys(tenVietTat);

      _driver.FindElement(By.Name("viTri")).SendKeys(Keys.Control + "a");
      _driver.FindElement(By.Name("viTri")).SendKeys(Keys.Delete);
      _driver.FindElement(By.Name("viTri")).SendKeys(viTri);

      _driver.FindElement(By.Name("moTa")).SendKeys(Keys.Control + "a");
      _driver.FindElement(By.Name("moTa")).SendKeys(Keys.Delete);
      _driver.FindElement(By.Name("moTa")).SendKeys(moTa);
    }

    public void SubmitForm()
    {
      _driver.FindElement(By.CssSelector("[data-testid='btn-submit']")).Click();
    }

    public void ClickEditButton(string tenKhoa)
    {
      var row = _wait.Until(d => d.FindElement(By.XPath($"//table//tr[td/div[contains(text(), '{tenKhoa}')]]")));
      var editButton = row.FindElement(By.CssSelector("[data-testid='btn-sua']"));
      editButton.Click();
    }


    public void ClickDeleteButton(string tenKhoa)
    {
      var row = _driver.FindElements(By.CssSelector("tbody tr"))
          .FirstOrDefault(r => r.Text.Contains(tenKhoa));
      if (row != null)
      {
        row.FindElement(By.CssSelector("[data-testid='btn-xoa']")).Click();
      }
    }

    public void ConfirmDelete()
    {
      var confirmBtn = _wait.Until(d =>
          d.FindElements(By.CssSelector(".ant-btn-primary")).FirstOrDefault());
      confirmBtn?.Click();
    }

    public void CancelDelete()
    {
      var cancelBtn = _wait.Until(d =>
          d.FindElements(By.CssSelector(".ant-btn")).FirstOrDefault());
      cancelBtn?.Click();
    }

    public bool IsMessageDisplayed(string message)
    {
      try
      {
        return _wait.Until(d => d.PageSource.Contains(message));
      }
      catch
      {
        return false;
      }
    }

    public void Search(string keyword)
    {
      var input = _driver.FindElement(By.CssSelector("input[placeholder='Tìm kiếm']"));
      input.Clear();
      input.SendKeys(keyword);

      _driver.FindElement(By.CssSelector("[data-testid='btn-tim']")).Click();
    }

    public void WaitUntilRowExists(string tenKhoa)
    {
      _wait.Until(d =>
      {
        try
        {
          var row = d.FindElement(By.XPath($"//table//tr[td/div[contains(text(), '{tenKhoa}')]]"));
          return row.Displayed;
        }
        catch (NoSuchElementException)
        {
          return false;
        }
      });
    }

    public bool IsRowPresent(string text)
    {
      try
      {
        return _wait.Until(d =>
            d.FindElements(By.CssSelector("tbody tr"))
             .Any(r => r.Text.Contains(text))
        );
      }
      catch
      {
        return false;
      }
    }
  }
}
