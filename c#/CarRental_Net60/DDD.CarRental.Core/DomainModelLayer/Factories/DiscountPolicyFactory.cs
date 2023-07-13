using DDD.CarRental.Core.DomainModelLayer.Interfaces;
using DDD.CarRental.Core.DomainModelLayer.Models;
using DDD.CarRental.Core.DomainModelLayer.Policies;

namespace DDD.CarRental.Core.DomainModelLayer.Factories
{
    public class DiscountPolicyFactory
    {
        public IDiscountPolicy Create(Driver driver)
        {
            IDiscountPolicy policy = new StandardDiscountPolicy(driver.FreeHours);
            if (driver.FirstName[driver.FirstName.Length - 1] == 'a') //dla kobiet profity
                policy = new VipDiscountPolicy(driver.FreeHours);
            return policy;
        }
    }
}
