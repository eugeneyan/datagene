class AccountController < Devise::RegistrationsController


  # POST /resource
  def create
    build_resource(sign_up_params)

    if resource.save
      yield resource if block_given?
      if resource.active_for_authentication?
        flash[:alert] = "Congratulations! You have successfully signed up for a new account. Start on the first game now!"
        sign_up(resource_name, resource)
        redirect_to root_path
      else
        set_flash_message :notice, :"signed_up_but_#{resource.inactive_message}" if is_flashing_format?
        expire_data_after_sign_in!
        respond_with resource, location: after_inactive_sign_up_path_for(resource)
      end
    else
      clean_up_passwords resource

      e = resource.errors.messages
      error_message = e.reduce("Please fill the form correctly:") { |i,v| "#{i}\n#{v[0].to_s} #{v[1][0].to_s}" }
      flash[:alert] = error_message
      redirect_to root_path
    end
  end


end