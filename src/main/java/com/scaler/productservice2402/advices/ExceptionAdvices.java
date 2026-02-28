package com.scaler.productservice2402.advices;

import com.scaler.productservice2402.dtos.ErrorResponseDto;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

@ControllerAdvice
public class ExceptionAdvices {

    @ExceptionHandler(RuntimeException.class)
    public ErrorResponseDto handleRuntimeException(RuntimeException ex){
        //handle error
        ErrorResponseDto errorResponseDto = new ErrorResponseDto();
        errorResponseDto.setStatus("Error");
        errorResponseDto.setMessage(ex.getMessage());
        return errorResponseDto;
    }
}
