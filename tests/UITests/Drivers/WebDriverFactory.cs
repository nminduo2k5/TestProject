using OpenQA.Selenium;
using OpenQA.Selenium.Edge;

namespace UITests.Drivers
{
  public static class WebDriverFactory
  {
    public static IWebDriver CreateEdgeDriver()
    {
      var options = new EdgeOptions();
      return new EdgeDriver(options);
    }
  }
}
