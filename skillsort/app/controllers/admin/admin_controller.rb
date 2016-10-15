module Admin
  class AdminController < ApplicationController
    before_filter :authenticate_user!
    before_filter :authorize_admin!


    protected

    def admin?
      return true if current_user.role == 'admin'
      false
    end


    def authorize_admin!
      unless admin?
        flash[:alert] = "You do not have privilege to access this resource."
        redirect_to root_url
      end
    end
  end
end