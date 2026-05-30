// File: KhoaUITest.cs
using NUnit.Framework;
using OpenQA.Selenium;
using OpenQA.Selenium.Edge;
using UITests.Pages;
using System;
using OpenQA.Selenium.Support.UI;

namespace UITests.Tests
{
  public class KhoaUITest
  {
    private IWebDriver? _driver;
    private KhoaPage? _page;

    [SetUp]
    public void Setup()
    {
      _driver = new EdgeDriver();
      _driver.Manage().Timeouts().ImplicitWait = TimeSpan.FromSeconds(10);
      _driver.Navigate().GoToUrl("http://localhost:5173/khoa");
      _page = new KhoaPage(_driver);
    }

    [Test]
    public void UC1_2_FUNC_001_Add_Valid_Khoa()
    {
      _page!.ClickAddButton();
      _page.EnterKhoa("Khoa CNTT", "Tầng 5", "CNTT", "Chứa các ngành IT");
      _page.SubmitForm();
      Assert.That(_page.IsMessageDisplayed("Thêm khoa thành công!"), Is.True);
    }

    [Test]
    public void UC1_2_FUNC_002_Add_Khoa_OnlyName()
    {
      _page!.ClickAddButton();
      _page.EnterKhoa("Khoa KHCB", "", "", "");
      _page.SubmitForm();
      Assert.That(_page.IsMessageDisplayed("Nhập thiếu thông tin!"), Is.True);
    }

    [Test]
    public void UC1_2_FUNC_003_Add_Duplicate_Khoa_Name()
    {
      _page!.ClickAddButton();
      _page.EnterKhoa("Khoa CNTT", "Tầng 1", "CNTT2", "Duplicated");
      _page.SubmitForm();
      Assert.That(_page.IsMessageDisplayed("Tên khoa đã tồn tại"), Is.True);
    }

    [Test]
    public void UC1_2_FUNC_004_Add_Khoa_OnlyAbbrev()
    {
      _page!.ClickAddButton();
      _page.EnterKhoa("", "", "KHTN", "");
      _page.SubmitForm();
      Assert.That(_page.IsMessageDisplayed("Nhập thiếu thông tin!"), Is.True);
    }

    [Test]
    public void UC1_2_FUNC_005_Add_Duplicate_Abbrev()
    {
      _page!.ClickAddButton();
      _page.EnterKhoa("Khoa Sinh2", "Tầng 3", "CNTT", "Duplicate");
      _page.SubmitForm();
      Assert.That(_page.IsMessageDisplayed("Tên viết tắt đã tồn tại"), Is.True);
    }

    [Test]
    public void UC1_2_FUNC_006_Add_Khoa_OnlyPosition()
    {
      _page!.ClickAddButton();
      _page.EnterKhoa("", "Tầng 4", "", "");
      _page.SubmitForm();
      Assert.That(_page.IsMessageDisplayed("Nhập thiếu thông tin!"), Is.True);
    }

    [Test]
    public void UC1_2_FUNC_007_Add_Khoa_OnlyDescription()
    {
      _page!.ClickAddButton();
      _page.EnterKhoa("", "", "", "Ngành khoa học");
      _page.SubmitForm();
      Assert.That(_page.IsMessageDisplayed("Nhập thiếu thông tin!"), Is.True);
    }

    [Test]
    public void UC1_2_FUNC_008_Edit_Khoa()
    {
      _page?.WaitUntilRowExists("Khoa Công nghệ"); // Đợi dòng xuất hiện trước khi chỉnh sửa
      _page?.ClickEditButton("Khoa Công nghệ");
      _page?.EnterKhoa("Khoa CNTT", "Tầng 12", "CNTT", "Đã sửa");
      _page?.SubmitForm();
      Assert.That(_page?.IsMessageDisplayed("Cập nhật thông tin Khoa thành công!"), Is.True);
    }

    [Test]
    public void UC1_2_FUNC_009_Delete_Khoa_Confirm()
    {
      _page!.ClickDeleteButton("Khoa Sinh");
      _page.ConfirmDelete();
      Assert.That(_page.IsMessageDisplayed("Xoá khoa thành công!"), Is.True);
    }

    [Test]
    public void UC1_2_FUNC_010_Delete_Khoa_Cancel()
    {
      _page!.ClickDeleteButton("Khoa Hóa");
      _page.CancelDelete();
      Assert.That(_page.IsMessageDisplayed("Xoá khoa thành công!"), Is.False);
    }

    [Test]
    public void UC1_2_FUNC_011_Fix_Error_Then_Submit()
    {
      _page!.ClickAddButton();
      _page.EnterKhoa("", "", "", "");
      _page.SubmitForm();
      Assert.That(_page.IsMessageDisplayed("Nhập thiếu thông tin!"), Is.True);

      _page.EnterKhoa("Khoa Toán", "Tầng 6", "TOAN", "Toán học");
      _page.SubmitForm();
      Assert.That(_page.IsMessageDisplayed("Thêm khoa thành công!"), Is.True);
    }

    [Test]
    public void UC1_2_FUNC_012_Search_Khoa_Exist()
    {
      _page!.Search("CNTT");
      Assert.That(_page.IsMessageDisplayed("CNTT"), Is.True);
    }

    [Test]
    public void UC1_2_FUNC_013_Search_Khoa_Not_Exist()
    {
      _page!.Search("KHONGTONTAI");
      Assert.That(_page.IsMessageDisplayed("Không tìm thấy kết quả!!"), Is.True);
    }

    [TearDown]
    public void TearDown()
    {
      _driver?.Quit();
    }
  }
}
