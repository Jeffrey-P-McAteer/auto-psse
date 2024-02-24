PROGRAM MAIN
  USE ALIB
  IMPLICIT NONE

  integer :: num_args

  character(len=280) :: input_json
  character(len=280) :: output_sav

  integer M

  num_args = command_argument_count()

  if (num_args.gt.0) then
    call get_command_argument(1,input_json)
    write (*,'("input_json = ", A)') input_json
  end if

  if (num_args.gt.1) then
    call get_command_argument(2,output_sav)
    write (*,'("output_sav = ", A)') output_sav
  end if


  M = FOO(3)
  WRITE (*,*) M

  CALL FOO2(6, M)
  WRITE (*,*) M

END PROGRAM MAIN
