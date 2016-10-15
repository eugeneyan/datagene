class AddBirthdayFieldsToUsers < ActiveRecord::Migration
  def change
  	add_column :users, :birthday_day, :integer
  	add_column :users, :birthday_month, :integer
  	add_column :users, :birthday_year, :integer
  end
end
