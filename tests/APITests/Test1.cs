using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using server;
using server.Controllers;
using server.Models;
using server.Repositories;

namespace APITests
{
    [TestClass]
    public sealed class Test1
    {
        private AppDbContext CreateInMemoryDbContext()
        {
            var options = new DbContextOptionsBuilder<AppDbContext>()
                .UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString())
                .Options;
            
            var context = new AppDbContext(options);
            context.Database.EnsureCreated();
            return context;
        }

        [TestMethod]
        public async Task Get_ReturnsAllBangCapOrderedCorrectly()
        {
            // Arrange
            using var context = CreateInMemoryDbContext();
            var repo = new PostgreRepository<BangCap>(context);
            var controller = new BangCapController(repo, context);

            // Seed initial data out of order
            context.BangCap.AddRange(new List<BangCap>
            {
                new BangCap { Id = Guid.NewGuid(), MaBangCap = "DEG_10", TenBangCap = "Tiến sĩ", TenVietTat = "TS" },
                new BangCap { Id = Guid.NewGuid(), MaBangCap = "DEG_2", TenBangCap = "Thạc sĩ", TenVietTat = "ThS" }
            });
            await context.SaveChangesAsync();

            // Act
            var response = await controller.Get();

            // Assert
            Assert.IsInstanceOfType(response.Result, typeof(OkObjectResult));
            var okResult = (OkObjectResult)response.Result;
            var list = (List<BangCap>)okResult.Value!;
            
            Assert.AreEqual(2, list.Count);
            // "DEG_2" is length 5, "DEG_10" is length 6, so "DEG_2" should be first due to length ordering
            Assert.AreEqual("DEG_2", list[0].MaBangCap);
            Assert.AreEqual("DEG_10", list[1].MaBangCap);
        }

        [TestMethod]
        public async Task Create_ValidBangCap_ReturnsCreatedAtAction()
        {
            // Arrange
            using var context = CreateInMemoryDbContext();
            var repo = new PostgreRepository<BangCap>(context);
            var controller = new BangCapController(repo, context);

            var newDto = new BangCapDto
            {
                TenBangCap = "Cử nhân",
                TenVietTat = "CN"
            };

            // Act
            var result = await controller.Create(newDto);

            // Assert
            Assert.IsInstanceOfType(result, typeof(CreatedAtActionResult));
            var createdResult = (CreatedAtActionResult)result;
            Assert.AreEqual(201, createdResult.StatusCode);

            // Verify database state (White-box: checking DB directly)
            var dbRecord = await context.BangCap.SingleOrDefaultAsync(b => b.TenBangCap == "Cử nhân");
            Assert.IsNotNull(dbRecord);
            Assert.AreEqual("CN", dbRecord.TenVietTat);
            Assert.AreEqual("DEG_1", dbRecord.MaBangCap); // 0 existing + 1
        }

        [TestMethod]
        public async Task Create_MissingFields_ReturnsBadRequest()
        {
            // Arrange
            using var context = CreateInMemoryDbContext();
            var repo = new PostgreRepository<BangCap>(context);
            var controller = new BangCapController(repo, context);

            // Missing TenVietTat
            var newDto = new BangCapDto
            {
                TenBangCap = "Cử nhân",
                TenVietTat = ""
            };

            // Act
            var result = await controller.Create(newDto);

            // Assert
            Assert.IsInstanceOfType(result, typeof(BadRequestObjectResult));
            var badRequest = (BadRequestObjectResult)result;
            Assert.AreEqual("Nhập thiếu thông tin", badRequest.Value);
        }

        [TestMethod]
        public async Task Create_DuplicateTenBangCap_ReturnsBadRequest()
        {
            // Arrange
            using var context = CreateInMemoryDbContext();
            var repo = new PostgreRepository<BangCap>(context);
            var controller = new BangCapController(repo, context);

            // Add existing
            context.BangCap.Add(new BangCap { Id = Guid.NewGuid(), MaBangCap = "DEG_1", TenBangCap = "Giáo sư", TenVietTat = "GS" });
            await context.SaveChangesAsync();

            var newDto = new BangCapDto
            {
                TenBangCap = "Giáo sư", // Duplicate
                TenVietTat = "PGS"
            };

            // Act
            var result = await controller.Create(newDto);

            // Assert
            Assert.IsInstanceOfType(result, typeof(BadRequestObjectResult));
            var badRequest = (BadRequestObjectResult)result;
            Assert.AreEqual("Tên bằng cấp đã tồn tại", badRequest.Value);
        }

        [TestMethod]
        public async Task Create_DuplicateTenVietTat_ReturnsBadRequest()
        {
            // Arrange
            using var context = CreateInMemoryDbContext();
            var repo = new PostgreRepository<BangCap>(context);
            var controller = new BangCapController(repo, context);

            // Add existing
            context.BangCap.Add(new BangCap { Id = Guid.NewGuid(), MaBangCap = "DEG_1", TenBangCap = "Giáo sư", TenVietTat = "GS" });
            await context.SaveChangesAsync();

            var newDto = new BangCapDto
            {
                TenBangCap = "Phó Giáo sư",
                TenVietTat = "GS" // Duplicate
            };

            // Act
            var result = await controller.Create(newDto);

            // Assert
            Assert.IsInstanceOfType(result, typeof(BadRequestObjectResult));
            var badRequest = (BadRequestObjectResult)result;
            Assert.AreEqual("Tên viết tắt đã tồn tại", badRequest.Value);
        }

        [TestMethod]
        public async Task Create_TenVietTatTooLong_ReturnsBadRequest()
        {
            // Arrange
            using var context = CreateInMemoryDbContext();
            var repo = new PostgreRepository<BangCap>(context);
            var controller = new BangCapController(repo, context);

            var newDto = new BangCapDto
            {
                TenBangCap = "Bằng cấp siêu dài",
                TenVietTat = "VIETTATSIEUDAI" // 14 characters, > 10
            };

            // Act
            var result = await controller.Create(newDto);

            // Assert
            Assert.IsInstanceOfType(result, typeof(BadRequestObjectResult));
            var badRequest = (BadRequestObjectResult)result;
            Assert.AreEqual("Tên viết tắt dài quá 10 ký tự!", badRequest.Value);
        }
    }
}
