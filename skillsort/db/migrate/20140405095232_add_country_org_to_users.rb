class AddCountryOrgToUsers < ActiveRecord::Migration
  def change
  	add_column :users, :country, :string
  	add_column :users, :organization, :string
  end
end
