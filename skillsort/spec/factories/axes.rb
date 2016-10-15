# Read about factories at https://github.com/thoughtbot/factory_girl

FactoryGirl.define do
  factory :axis do
    name "MyString"
    description "MyText"
    value 1
    active false
  end
end
