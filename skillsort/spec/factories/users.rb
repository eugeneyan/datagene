# Read about factories at https://github.com/thoughtbot/factory_girl

FactoryGirl.define do
  factory :user do
  	email 'email1@factory.com'
  	first_name 'John'
  	last_name 'Smith'
  	password "password"
    password_confirmation "password"
    birthday_day 1
    birthday_month 1
    birthday_year 1965
    gender 'Male'
  end
end
