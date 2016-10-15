# Read about factories at https://github.com/thoughtbot/factory_girl

FactoryGirl.define do
  factory :feedback do
    user_id 1
    qn1 1
    qn2 1
    qn3 1
    qn4 1
    qn5 1
    qn6 1
    qn7 "MyString"
    qn8 "MyText"
    qn9 "MyText"
    qn10 "MyText"
    qn11 "MyText"
  end
end
